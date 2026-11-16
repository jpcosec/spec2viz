// <sldb-annotations>
// The catalog's annotations saved in an sldb store through `sldb serve --cors` (specIR, IR13b).
// Reads with GET /document?id=<doc>; writes with POST /save, guarded by the payload it read
// (`expected`): a 409 means someone else saved first, so it merges with what is stored and retries
// once. The browser's localStorage stays as the local copy; the store wins when the page loads.
function sldbAnnotationsConfig(config, search) {
  const params = new URLSearchParams(search || '');
  const server = (params.get('sldb') || (config && config.server) || '').replace(/\/+$/, '');
  return { ...(config || {}), server, doc: params.get('annotations') || (config && config.doc) || '' };
}

function sldbAnnotationsStore(config, fetchImpl) {
  let current = null;
  const url = path => `${config.server}${path}`;

  async function read() {
    const response = await fetchImpl(url(`/document?id=${encodeURIComponent(config.doc)}`));
    if (response.status === 404) {
      current = null;
      return [];
    }
    if (!response.ok) throw new Error(`sldb serve answered ${response.status} reading ${config.doc}`);
    current = (await response.json()).payload;
    return Array.isArray(current.annotations) ? current.annotations : [];
  }

  function change(items) {
    if (!current) {
      const payload = { title: config.title || config.doc, catalog: config.catalog || '', annotations: items };
      return { id: config.doc, action: 'create', model: config.model, payload };
    }
    return { id: config.doc, action: 'update', model: config.model, payload: { ...current, annotations: items }, expected: current };
  }

  function post(items) {
    const body = JSON.stringify({ changes: [change(items)] });
    return fetchImpl(url('/save'), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body });
  }

  function merge(stored, local) {
    const seen = new Set();
    return [...stored, ...local].filter(a => {
      const key = JSON.stringify([a.key, a.comentario, a.ts]);
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  async function write(items) {
    let response = await post(items);
    if (response.status === 409) {
      items = merge(await read(), items);
      response = await post(items);
    }
    if (!response.ok) throw new Error(`sldb serve answered ${response.status} saving ${config.doc}: ${await response.text()}`);
    await read();
    return items;
  }

  return { read, write, merge };
}

function installSldbAnnotations(config, fetchImpl) {
  if (!config.server || !config.doc || typeof annoWriteStore !== 'function') return null;
  const store = sldbAnnotationsStore(config, fetchImpl);
  const keepLocal = annoWriteStore;
  let queue = Promise.resolve();
  globalThis.annoWriteStore = function (items) {
    keepLocal(items);
    queue = queue
      .then(() => store.write(items))
      .then(saved => { if (saved !== items) { keepLocal(saved); annoRender(); } })
      .catch(error => console.warn('[specir] annotations not saved in sldb:', error.message));
    return queue;
  };
  globalThis.annoLoad = function () {
    return store.read()
      .then(items => { keepLocal(items); annoRender(); })
      .catch(error => {
        console.warn('[specir] annotations not read from sldb, using the local copy:', error.message);
        annoCache = annoReadStore();
        annoRender();
      });
  };
  return store;
}

installSldbAnnotations(sldbAnnotationsConfig(window.SPECIR_ANNOTATIONS, (globalThis.location || {}).search), globalThis.fetch && globalThis.fetch.bind(globalThis));
// </sldb-annotations>

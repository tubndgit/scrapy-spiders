var config = {
    mode: "fixed_servers",
    rules: {
      singleProxy: {
        scheme: "http",
        host: "localhost",
        port: 8123
      },
      bypassList: ["foobar.com"]
    }
  };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "alan222",
            password: "alan222"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
);
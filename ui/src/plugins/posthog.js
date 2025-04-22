//./plugins/posthog.js
import posthog from "posthog-js";

export default {
  install(app) {
    app.config.globalProperties.$posthog = posthog.init(
      'phc_f6wn4l28KKcjHCRRxAgBZEcP28nAnP9RaYD3dv43YZb',
      {
        api_host: 'https://eu.i.posthog.com',
      }
    );
    // get userinfo from '/userinfo'
    fetch('/userinfo').then(res => res.json()).then(data => {
      posthog.identify(data["email"])
    })
  },
};

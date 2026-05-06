import axios from 'axios'

axios.interceptors.response.use(
  res => res,
  async err => {
    if (err.response && err.response.status === 401) {
      try {
        console.log('refreshing token')
        // Attempt silent refresh of JWT token
        await axios.get('/refreshtoken');
        // Retry original request
        let resp = await axios(err.config);
        return resp;

      } catch (refreshErr) {
        // If refresh fails, redirect to login
        window.location.href = '/';
      }
    }
    return Promise.reject(err);
  }
);

export default axios
import axios from "axios";

const api = axios.create({
  baseURL: "http://35.175.150.159:8000/api/",
});

export default api;

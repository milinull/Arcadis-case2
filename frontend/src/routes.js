import Case1 from "views/Case1.js";
import Case2 from "views/Case2.js";
import Case3 from "views/Case3.js";

var routes = [
  {
    path: "/index",
    name: "Report PDF",
    icon: "ni ni-single-copy-04 text-red",
    component: <Case1 />,
    layout: "/case1",
  },
  {
    path: "/index",
    name: "Risk Analytics",
    icon: "ni ni-chart-bar-32 text-orange",
    component: <Case2 />,
    layout: "/case2",
  },
  {
    path: "/index",
    name: "Data Management",
    icon: "ni ni-cloud-upload-96 text-green",
    component: <Case3 />,
    layout: "/case3",
  },
];
export default routes;

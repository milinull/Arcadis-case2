import Index from "views/Index.js";
import Case1 from "views/Case1.js";

var routes = [
  {
    path: "/index",
    name: "Risk Analytics",
    icon: "ni ni-chart-bar-32 text-orange",
    component: <Index />,
    layout: "/case2",
  },
  {
    path: "/case1",
    name: "Case 1",
    icon: "ni ni-spaceship text-blue",
    component: <Case1 />,
    layout: "/case1",
  },
];
export default routes;

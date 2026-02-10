import React, { useState } from "react";
import { NavLink as NavLinkRRD, Link } from "react-router-dom";
import { PropTypes } from "prop-types";
import {
  Collapse,
  NavbarBrand,
  Navbar,
  NavItem,
  NavLink,
  Nav,
  Container,
  Row,
  Col,
} from "reactstrap";

const Sidebar = ({ routes, logo }) => {
  const [collapseOpen, setCollapseOpen] = useState(false);

  const toggleCollapse = () => setCollapseOpen(!collapseOpen);
  const closeCollapse = () => setCollapseOpen(false);

  const createLinks = (routes) => {
    return routes.map((prop, key) => (
      <NavItem key={key}>
        <NavLink
          to={prop.layout + prop.path}
          tag={NavLinkRRD}
          onClick={closeCollapse}
          activeClassName="active"
        >
          <i className={prop.icon} />
          {prop.name}
        </NavLink>
      </NavItem>
    ));
  };

  return (
    <Navbar
      className="navbar-vertical fixed-left navbar-light bg-white"
      expand="md"
      id="sidenav-main"
    >
      <Container fluid>
        <button
          className="navbar-toggler"
          type="button"
          onClick={toggleCollapse}
        >
          <span className="navbar-toggler-icon" />
        </button>

        {logo && (
          <NavbarBrand className="pt-0" tag={Link} to={logo.innerLink}>
            <img
              alt={logo.imgAlt}
              className="navbar-brand-img"
              src={logo.imgSrc}
            />
          </NavbarBrand>
        )}

        <Collapse navbar isOpen={collapseOpen}>
          <div className="navbar-collapse-header d-md-none">
            <Row>
              {logo && (
                <Col className="collapse-brand" xs="6">
                  <Link to={logo.innerLink}>
                    <img alt={logo.imgAlt} src={logo.imgSrc} />
                  </Link>
                </Col>
              )}
              <Col className="collapse-close" xs="6">
                <button
                  className="navbar-toggler"
                  type="button"
                  onClick={toggleCollapse}
                >
                  <span />
                  <span />
                </button>
              </Col>
            </Row>
          </div>

          <Nav navbar>{createLinks(routes)}</Nav>
          <hr className="my-3" />
          <Nav navbar>
            <NavItem>
              <NavLink
                href="https://github.com/milinull/Arcadis-case"
                target="_blank"
                onClick={closeCollapse}
              >
                <i className="fab fa-github" style={{ fontSize: "1.1rem" }} />
                Github
              </NavLink>
            </NavItem>
          </Nav>
        </Collapse>
      </Container>
    </Navbar>
  );
};

Sidebar.propTypes = {
  routes: PropTypes.arrayOf(PropTypes.object),
  logo: PropTypes.shape({
    innerLink: PropTypes.string,
    imgSrc: PropTypes.string.isRequired,
    imgAlt: PropTypes.string.isRequired,
  }),
};

export default Sidebar;

import React from "react";
import { Card, CardHeader, CardBody, Container, Row, Col } from "reactstrap";

const Case1 = () => {
  return (
    <>
      <div className="header bg-gradient-info pb-8 pt-5 pt-md-8">
        <Container fluid>
          <div className="header-body">
            <h1 className="text-white">Case 1</h1>
          </div>
        </Container>
      </div>

      <Container className="mt--7" fluid>
        <Row>
          <Col className="mb-5 mb-xl-0" xl="12">
            <Card className="shadow">
              <CardHeader className="bg-transparent">
                <h3 className="mb-0">Título</h3>
              </CardHeader>
              <CardBody></CardBody>
            </Card>
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default Case1;

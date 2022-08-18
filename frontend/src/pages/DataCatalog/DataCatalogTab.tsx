import React from "react";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import Card from "@material-ui/core/Card";
import Typography from "@material-ui/core/Typography";
import DatasetExplorer from "./dataset_explorer/DatasetExplorer";
import MethodologyTab from "./MethodologyTab";
import { DATA_SOURCE_PRE_FILTERS, useSearchParams } from "../../utils/urlutils";
import {
  DATA_CATALOG_PAGE_LINK,
  METHODOLOGY_TAB_LINK,
  AGE_ADJUSTMENT_TAB_LINK,
} from "../../utils/internalRoutes";
import styles from "../AboutUs/AboutUsPage.module.scss";
import { Link, Route, Switch } from "react-router-dom";
import FeedbackBox from "../ui/FeedbackBox";
import AgeAdjustmentTab from "./AgeAdjustmentTab";

function DataCatalogTab() {
  const params = useSearchParams();
  const datasets = params[DATA_SOURCE_PRE_FILTERS]
    ? params[DATA_SOURCE_PRE_FILTERS].split(",")
    : [];
  return (
    <div className={styles.AboutUsPage}>
      <Route path="/">
        <Tabs
          centered
          indicatorColor="primary"
          textColor="primary"
          value={window.location.pathname}
        >
          <Card
            elevation={3}
            style={{
              width: "220px",
              textAlign: "left",
              border: "1px solid #5f6368",
              height: "130px",
              marginRight: "50px",
            }}
          >
            <Typography
              variant="h4"
              className={styles.DatasetTitle}
              align="left"
              style={{
                fontSize: "1.125rem",
                color: "#14763d",
                paddingLeft: "5px",
                fontWeight: "bold",
              }}
            >
              Data
            </Typography>
            <div style={{ paddingLeft: "15px" }}>
              <div style={{ color: "#63bb6e", fontWeight: "bold" }}>
                Sources and Downloads
              </div>
              <div>Limitations</div>
              <div>Recommendations</div>
            </div>
          </Card>
          <Card
            elevation={3}
            style={{
              width: "220px",
              textAlign: "left",
              border: "1px solid gray",

              marginRight: "50px",
            }}
          >
            <Typography
              variant="h4"
              className={styles.DatasetTitle}
              align="left"
              style={{
                fontSize: "1.125rem",
                color: "#14763d",
                paddingLeft: "5px",
                fontWeight: "bold",
              }}
            >
              Methodology
            </Typography>
            <div style={{ paddingLeft: "15px", width: "220px" }}>
              <div>Acquisition and</div>
              <div>Standardization</div>
              <div>Age Adjustment</div>
              <div>Disclaimers and Alerts</div>
            </div>
          </Card>
          <Card
            elevation={3}
            style={{
              width: "220px",
              textAlign: "left",
              border: "1px solid gray",
              height: "130px",
              marginRight: "50px",
            }}
          >
            <Typography
              variant="h4"
              className={styles.DatasetTitle}
              align="left"
              style={{
                fontSize: "1.125rem",
                color: "#14763d",
                paddingLeft: "5px",
                fontWeight: "bold",
              }}
            >
              Glossary
            </Typography>
            <div style={{ paddingLeft: "15px" }}>
              <div>Topics</div>
              <div>Key Terms and Definitions</div>
              <div>Resources</div>
            </div>
          </Card>
          <Card
            elevation={3}
            style={{
              width: "220px",
              textAlign: "left",
              border: "1px solid gray",
              height: "130px",
              marginRight: "50px",
            }}
          >
            <Typography
              variant="h4"
              className={styles.DatasetTitle}
              align="left"
              style={{
                fontSize: "1.125rem",
                color: "#14763d",
                paddingLeft: "5px",
                fontWeight: "bold",
              }}
            >
              Take Action
            </Typography>
            <div style={{ paddingLeft: "15px" }}>
              <div>Cite the Tracker</div>
              <div>Research</div>
              <div>News and Stories</div>
            </div>
          </Card>
        </Tabs>
      </Route>

      <Switch>
        <Route path={`${METHODOLOGY_TAB_LINK}/`}>
          <MethodologyTab />
        </Route>
        <Route path={`${DATA_CATALOG_PAGE_LINK}/`}>
          <DatasetExplorer preFilterDataSourceIds={datasets} />
        </Route>
        <Route path={`${AGE_ADJUSTMENT_TAB_LINK}/`}>
          <AgeAdjustmentTab />
        </Route>
      </Switch>
      <FeedbackBox />
    </div>
  );
}

export default DataCatalogTab;

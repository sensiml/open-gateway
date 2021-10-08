import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import {VersionCheck} from "./services/VersionCheck";
import {apiHosts} from "./configs";

const versionCheck = new VersionCheck(apiHosts.baseHost, apiHosts.cloudHost);

ReactDOM.render(
  <App versionCheck={versionCheck}/>,
  document.getElementById('root'),
);

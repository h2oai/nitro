// Copyright 2022 H2O.ai, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { createTheme, loadTheme, registerIcons } from '@fluentui/react';
import React from 'react';
import ReactDOM from 'react-dom';
import { App } from './app';
import { newClient } from './client';
import { icons } from './icons';
import reportWebVitals from './reportWebVitals';


// https://fabricweb.z5.web.core.windows.net/pr-deploy-site/refs/heads/master/theming-designer/
const
  purple = createTheme({
    defaultFontStyle: { fontFamily: '"Roboto"' },
  });

loadTheme(purple)
registerIcons({ icons })

const root = document.getElementById('nitro')
const client = newClient(root?.getAttribute('data-endpoint') ?? '/nitro')
ReactDOM.render(<App client={client} />, root);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

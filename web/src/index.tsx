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

import { registerIcons } from '@fluentui/react';
import ReactDOM from 'react-dom';
import { App } from './app';
import { newClient } from './client';
import { icons } from './icons';
import { newLocalServer } from './nitride';
import reportWebVitals from './reportWebVitals';
import { newSocketServer } from './socket';
import { loadScheme } from './theme';

registerIcons({ icons })

const
  root = document.getElementById('nitro'),
  endpoint = root?.getAttribute('data-endpoint'), // TODO document
  server = endpoint ? newSocketServer(endpoint) : newLocalServer(),
  client = newClient(server)

loadScheme(client.schemeB())
ReactDOM.render(<App client={client} />, root);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

# Copyright 2018 Canonical Ltd.
# Licensed under the LGPLv3, see LICENCE.txt file for details.

"""Templates for generating the JavaScript API client."""

from jinja2 import Template


facade_template = Template("""
'use strict';


class {{ name }}V{{ version }} {

  constructor(transport, info) {
    this._transport = transport;
    this._info = info;
    this.version = {{ version }};
  }
  {%- for method in methods %}

  /**
    {%- if method.params %}
    @param {Object} args Arguments to be provided to Juju, as an object like
      the following:
        {{ method.params.docstring()|indent(8) }}
    {%- endif %}
    {%- if method.result %}
    @param {Function} callback Called when the response from Juju is available,
      the callback receives an error and the result. If there are no errors,
      the result is provided as an object like the following:
        {{ method.result.docstring()|indent(8) }}
    {%- else %}
    @param {Function} callback Called when the response from Juju is available,
      the callback receives an error or null if the operation succeeded.
    {%- endif %}
  */
  {{ method.name() }}({% if method.params %}args, {% endif %}callback) {
    {%- if method.params %}
    // Prepare request parameters.
    let params;
    {{ method.params.marshal('params', 'args')|indent() }}
    {%- else %}
    const params = {};
    {%- endif %}
    // Prepare the request to the Juju API.
    const req = {
      type: '{{ name }}',
      request: '{{ method.request }}',
      version: {{ version }},
      params: params
    };
    // Send the request to the server.
    this._transport.write(req, (err, resp) => {
      if (!callback) {
        return;
      }
      if (err) {
        callback(err, {});
        return;
      }
      {%- if method.result %}
      // Handle the response.
      let result;
      {{ method.result.unmarshal('result', 'resp')|indent(6) }}
      callback(null, result);
      {%- else %}
      callback(null, {});
      {%- endif %}
    });
  }
  {%- endfor %}
}


const wrappers = require('../wrappers.js');
if (wrappers.wrap{{ name }}) {
  {{ name }}V{{ version }} = wrappers.wrap{{ name }}({{ name }}V{{ version }});
}

module.exports = {{ name }}V{{ version }};
"""[1:])
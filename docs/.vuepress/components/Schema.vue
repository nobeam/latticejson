<template>
  <div class="schema">
    <table style="width:100%">
      <thead>
        <tr>
          <th>Property</th>
          <th>Required</th>
          <th>Type</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(value, name) in this.schema.properties">
          <td>{{name}}</td>
          <td>{{schema.required.includes(name)}}</td>
          <td>{{value.type}}</td>
          <td>{{value.description}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import SCHEMA from "../../../latticejson/schema.json";
export default {
  name: "Schema",
  data() {
    return { schema: SCHEMA };
  }
};
</script>

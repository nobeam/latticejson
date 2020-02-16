<template>
  <div class="definition">
    <h3 :id="name.toLowerCase()">
      <a :href="'#'+name.toLowerCase()" class="header-anchor">#</a>
      {{name}}
    </h3>
    <p>{{definition.description}}</p>
    <table style="width:100%">
      <thead>
        <tr>
          <th>Attribute</th>
          <th>Type</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="value, name in definition">
          <td>{{name}}</td>
          <td>{{value.type}}</td>
          <td>{{value.description}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "Definition",
  props: {
    name: String,
    definition: Object
  }
};
</script>

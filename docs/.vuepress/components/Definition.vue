<template>
  <div class="definition">
    <h3 :id="type.toLowerCase()">
      <a :href="'#'+type.toLowerCase()" class="header-anchor">#</a>
      {{type}}
    </h3>
    <p>{{description}}</p>
    <table style="width:100%">
      <thead>
        <tr>
          <th>Attribute</th>
          <th>Type</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="attribute, name in attributes">
          <td>{{name}}</td>
          <td>{{attribute.type}}</td>
          <td>{{attribute.description}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "Definition",
  props: {
    type: String,
    attributes: Object,
    description: String
  }
};
</script>

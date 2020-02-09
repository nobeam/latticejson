<template>
  <div class="definition">
    <h1>{{name}}</h1>
    <p>{{definition.description}}</p>
    <table style="width:100%">
      <tr>
        <th>Attribute</th>
        <th>Type</th>
        <th>Description</th>
      </tr>
      <tr v-for="value, name in definition.items[1].properties">
        <th>{{name}}</th>
        <th>{{value.type}}</th>
        <th>{{value.description}}</th>
      </tr>
    </table>
  </div>
</template>

<script>
export default {
  name: "Definition",
  props: {
    name: String,
    definition: Object
  },
  methods: {
    getAttributes() {
      return 0;
    }
  }
};
</script>

<style>
</style>
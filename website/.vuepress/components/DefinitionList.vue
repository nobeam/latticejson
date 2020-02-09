<template>
  <div class="definiFor recursive compotion-list">
    <definition
      v-for="definition, name in schema.definitions"
      :definition="definition"
      :name="name"
    />
  </div>
</template>

<script>
import SCHEMA from "/home/felix/Git/nobeam/latticejson/latticejson/schema.json";
import Definition from "./Definition.vue";
export default {
  name: "DefinitionList",
  components: Definition,
  data() {
    return { schema: SCHEMA };
  }
};
</script>

<style>
</style>For recursive compo
<template>
  <div class="definition-list">
    <definition
      v-for="definition, name in this.elements"
      :definition="definition"
      :name="name"
      :schema="schema"
    />
  </div>
</template>

<script>
// TODO: change uri
import SCHEMA from "/home/felix/Git/nobeam/latticejson/latticejson/schema.json";
import Definition from "./Definition.vue";
export default {
  name: "DefinitionList",
  components: Definition,
  data() {
    return { schema: SCHEMA };
  },
  computed: {
    elements() {
      const elements = {};
      const base = this.schema.definitions["Element"];
      for (const [type, definition] of Object.entries(
        this.schema.definitions
      )) {
        if (
          !definition.hasOwnProperty("allOf") ||
          !definition["allOf"][0].hasOwnProperty("$ref") ||
          !definition["allOf"][0]["$ref"] === "#/definitions/Element"
        ) {
          continue;
        }

        elements[type] = {};
        for (const [key, property] in Object.entries(
          definition.items[1].properties
        )) {
          elements[type][key] = property;
        }
      }
      return elements;
    }
  }
};
</script>

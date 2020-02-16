<template>
  <div class="definition-list">
    <definition
      v-for="type in this.elements"
      :type="type"
      :attributes="elementsAttributes[type]"
      :description="elementsDescription[type]"
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
    definitions() {
      return this.schema.definitions;
    },
    elements() {
      const elements = [];
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

        elements.push(type);
      }
      return elements;
    },
    elementsAttributes() {
      const attributes = {};
      const attributes_base = this.schema.definitions["Element"].items[1]
        .properties;
      for (const element of this.elements) {
        const attributes_own = this.definitions[element].items[1].properties;
        attributes[element] = {};
        for (const [key, attribute] of Object.entries(attributes_own)) {
          const is_own = Object.entries(attribute).length !== 0;
          attributes[element][key] = is_own ? attribute : attributes_base[key];
        }
      }
      return attributes;
    },
    elementsDescription() {
      const descriptions = {};
      for (const element of this.elements) {
        descriptions[element] = this.definitions[element].description;
      }
      return descriptions;
    }
  }
};
</script>

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
import Definition from "./Definition.vue";
import SCHEMA from "../../../latticejson/schema.json";
export default {
  name: "DefinitionList",
  components: Definition,
  data() {
    return { schema: SCHEMA };
  },
  created() {
    this.schema = SCHEMA;
    this.definitions = this.schema.definitions;
    this.elements = [];
    for (const [type, definition] of Object.entries(this.schema.definitions)) {
      if (
        !definition.hasOwnProperty("allOf") ||
        !definition["allOf"][0].hasOwnProperty("$ref") ||
        !definition["allOf"][0]["$ref"] === "#/definitions/Element"
      ) {
        continue;
      }

      this.elements.push(type);
    }

    this.elementsAttributes = {};
    const attributes_base = this.schema.definitions["Element"].items[1]
      .properties;
    for (const element of this.elements) {
      const attributes_own = this.definitions[element].items[1].properties;
      this.elementsAttributes[element] = {};
      for (const [key, attribute] of Object.entries(attributes_own)) {
        const is_own = Object.entries(attribute).length !== 0;
        this.elementsAttributes[element][key] = is_own
          ? attribute
          : attributes_base[key];
      }
    }

    this.elementsDescription = {};
    for (const element of this.elements) {
      this.elementsDescription[element] = this.definitions[element].description;
    }
  }
};
</script>

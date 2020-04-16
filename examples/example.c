#include <stdio.h>
#include <json-c/json.h>

const int buffer_size = 20 * 1024;

int main(int argc, char **argv) {
    char buffer[buffer_size];
    FILE *fp = fopen("fodo.json", "r");
    fread(buffer, buffer_size, 1, fp);
    fclose(fp);

    struct json_object *parsed_json;
    struct json_object *elements;
    struct json_object *element;
    struct json_object *type;
    struct json_object *attributes;
    struct json_object *length;
    struct json_object *sub_lattices;
    struct json_object *lattice;

    const char *element_name = "Q1";
    parsed_json = json_tokener_parse(buffer);
    json_object_object_get_ex(parsed_json, "elements", &elements);
    json_object_object_get_ex(elements, element_name, &element);
    type = json_object_array_get_idx(element, 0);
    attributes = json_object_array_get_idx(element, 1);
    json_object_object_get_ex(attributes, "length", &length);

    printf(
        "The element %s is a %s and is %f meters long.\n",
        element_name,
        json_object_get_string(type),
        json_object_get_double(length)
    );
}

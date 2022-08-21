#!/usr/bin/env python3
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, metavar="input_file", required=True, help="Input JSON array filename")
parser.add_argument("-o", "--output", type=str, metavar="output_file", required=True, help="Output JSON array filename")
args = parser.parse_args()

source_json_file_name = args.input if args.input else args.i
output_json_file_name = args.output if args.output else args.o

with open(source_json_file_name) as source_json_file:
    json_data = json.load(source_json_file)
    print("JSON array items count read = ", len(json_data))
    terraform_json_data = []
    for i in range(len(json_data)):
        if "migrationVersion" in json_data[i]:
            terraform_json_data.append({
                "_id": json_data[i]["type"] + ":" + json_data[i]["id"],
                "_source": {
                    "type": json_data[i]["type"],
                    "migrationVersion": json_data[i]["migrationVersion"],
                    "references": json_data[i]["references"],
                    json_data[i]["type"]: json_data[i]["attributes"],
                    "updated_at": json_data[i]["updated_at"]
                }
            })
        else:
            terraform_json_data.append({
                "_id": json_data[i]["type"] + ":" + json_data[i]["id"],
                "_source": {
                    "type": json_data[i]["type"],
                    "references": json_data[i]["references"],
                    json_data[i]["type"]: json_data[i]["attributes"],
                    "updated_at": json_data[i]["updated_at"]
                }
            })

if len(terraform_json_data) > 0:
    print("JSON array items count write = ", len(terraform_json_data))
    with open(output_json_file_name, 'w') as outfile:
        #json.dump(terraform_json_data, outfile)
        print(json.dumps(terraform_json_data, indent = 2), file = outfile)
else:
    print("Nothing to save.")
# elasticsearch-kibana-object-terraform-convert

## Description

This python script is using when there is a need to convert saved objects from Kibana UI to export.ndjson and to convert to terraform elasticsearch_kibana_object resource template like this:

```terraform
resource "elasticsearch_kibana_object" "test_visualization_v6" {
  body = <<EOF
[
  {
    "_id": "visualization:response-time-percentile",
    "_type": "doc",
    "_source": {
      "type": "visualization",
      "visualization": {
        "title": "Total response time percentiles",
        "visState": "{\"title\":\"Total response time percentiles\",\"type\":\"line\",\"params\":{\"addTooltip\":true,\"addLegend\":true,\"legendPosition\":\"right\",\"showCircles\":true,\"interpolate\":\"linear\",\"scale\":\"linear\",\"drawLinesBetweenPoints\":true,\"radiusRatio\":9,\"times\":[],\"addTimeMarker\":false,\"defaultYExtents\":false,\"setYExtents\":false},\"aggs\":[{\"id\":\"1\",\"enabled\":true,\"type\":\"percentiles\",\"schema\":\"metric\",\"params\":{\"field\":\"app.total_time\",\"percents\":[50,90,95]}},{\"id\":\"2\",\"enabled\":true,\"type\":\"date_histogram\",\"schema\":\"segment\",\"params\":{\"field\":\"@timestamp\",\"interval\":\"auto\",\"customInterval\":\"2h\",\"min_doc_count\":1,\"extended_bounds\":{}}},{\"id\":\"3\",\"enabled\":true,\"type\":\"terms\",\"schema\":\"group\",\"params\":{\"field\":\"system.syslog.program\",\"size\":5,\"order\":\"desc\",\"orderBy\":\"_term\"}}],\"listeners\":{}}",
        "uiStateJSON": "{}",
        "description": "",
        "version": 1,
        "kibanaSavedObjectMeta": {
            "searchSourceJSON": "{\"index\":\"filebeat-*\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"
        }
      }
    }
  }
]
EOF
}
```

## Preparing

Add "[" in the begginning of exported .ndjson and "]" at the end of file to match json array format and save this file as source.json.

## Running script

```bash
chmod +x es_json_transform.py
./es_json_transform.py -i es_kibana_ops_objects.json -o es_kibana_ops_objects_transf.json

JSON array items count read =  270
JSON array items count write =  270
```

## Using converted json template to import kibana objects

Example of terraform code to use json template:

```terraform
locals {
  kibana_objects_json = file("${path.module}/config/es_kibana_${local.tf_workspace}_objects.json")
  kibana_objects_data = jsondecode(local.kibana_objects_json)
}

resource "elasticsearch_kibana_object" "es_object" {
  depends_on = [aws_elasticsearch_domain.es_kibana]
  count = var.import_es_kibana_objects ? length(local.kibana_objects_data) : 0
  body = jsonencode([local.kibana_objects_data[count.index]])
  lifecycle {
    ignore_changes = [
      body,
    ]
  }
}
```

# {{RESOURCE_NAME}}

## Overview
{{SHORT_DESCRIPTION_OF_RESOURCE}}

## Contexts
| Context | Base Path | Authentication | Description |
|--------|----------|----------------|-------------|
| `me` | `/v1/me/{{resource_slug}}/` | Required | {{ME_DESCRIPTION}} |
| `reference` | `/v1/reference/{{resource_slug}}/` | Optional / Public | System-owned reference resources (managed by account defined by TMTA_USERNAME environment variable) |

## Endpoints

#### List
`GET {base}`

#### Retrieve
`GET {base}{id}/`

{{ADDITIONAL_ENDPOINTS}}

### Context Differences

#### Reference
- Managed internally by system account (defined by TMTA_USERNAME environment variable)
{{REFERENCE_DIFFERENCES}}

#### Me
{{ME_DIFFERENCES}}
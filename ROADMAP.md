# Roadmap

Every endpoint in the PlentyMarkets OpenAPI spec ([`openApiV3.json`](https://raw.githubusercontent.com/plentymarkets/api-doc/master/plentymarkets/openApiV3/openApiV3.json)), grouped by API tag, with implementation status and the method that implements it in this codebase. Generated from the spec + a scan of `src/plentymarkets/modules/*.py`, so it stays accurate as coverage grows.

**180 / 1837** endpoints implemented across **53** API tags.

| API Tag | Description | Coverage |
|---|---|---|
| [`Account`](#account) | Customer accounts and contacts — addresses, contact data, bank details | **4/151** |
| [`Accounting`](#accounting) | VAT configurations, financial accounts, revenue bookings | 0/35 — planned |
| [`AddressDesign`](#addressdesign) | Address label templates and print format settings | 0/9 — planned |
| [`AuditLog`](#auditlog) | Change history and audit trail for system actions | 0/8 — planned |
| [`Authentication`](#authentication) | Login/logout and token management | internal (used by `_session.py`) |
| [`Authorization`](#authorization) | User roles, permissions, and access rights | 0/3 — planned |
| [`Basket`](#basket) | Shopping cart / basket management for webshop visitors | 0/4 — planned |
| [`Batch`](#batch) | Batch processing and bulk operations across resources | 0/1 — planned |
| [`BI`](#bi) | Business intelligence — reports and analytics data | 0/31 — planned |
| [`Blog`](#blog) | Blog posts and categories published in the webshop | 0/5 — planned |
| [`Board`](#board) | Task boards (Kanban-style) for internal team workflows | 0/16 — planned |
| [`Boards`](#boards) | Board management — creating and configuring boards | 0/6 — planned |
| [`Catalog`](#catalog) | Data catalogues for flexible export/import field mappings | 0/33 — planned |
| [`Category`](#category) | Product and content categories used in webshop and items | 0/13 — planned |
| [`Cloud`](#cloud) | Cloud storage and file management | 0/21 — planned |
| [`Comment`](#comment) | Comments attachable to orders, contacts, and tickets | 0/5 — planned |
| [`Configuration`](#configuration) | System-wide settings and global configuration values | 0/5 — planned |
| [`Document`](#document) | Order documents — invoices, delivery notes, return slips | 0/44 — planned |
| [`ElasticSync`](#elasticsync) | Data import/sync mappings (Data Exchange / ElasticSync) | 0/75 — planned |
| [`Export`](#export) | Data export formats, fields, and export jobs | 0/6 — planned |
| [`ExportSettings`](#exportsettings) | Settings and saved configurations for exports | 0/6 — planned |
| [`Feedback`](#feedback) | Customer product reviews and ratings | 0/17 — planned |
| [`Fulfillment`](#fulfillment) | Shipping labels, package tracking, shipping service providers | 0/10 — planned |
| [`Item`](#item) | Product catalogue — items, variations, images, attributes, prices (legacy `/rest/items` tree) | **4/294** |
| [`LegalInformation`](#legalinformation) | Legal texts — terms of service, privacy policy, cancellation rights | 0/4 — planned |
| [`Listing`](#listing) | eBay/marketplace listing templates and active listings | 0/48 — planned |
| [`Log`](#log) | System log entries and error/debug logs | 0/8 — planned |
| [`MailTemplates`](#mailtemplates) | Email templates for automated system notifications | 0/9 — planned |
| [`Market`](#market) | Marketplace integrations — Amazon, eBay, Otto, etc. | 0/43 — planned |
| [`Messenger`](#messenger) | Internal messaging between system users | 0/92 — planned |
| [`Newsletter`](#newsletter) | Newsletter recipient lists and subscription management | 0/21 — planned |
| [`Order`](#order) | Orders, order items, order properties, and status management | **75/307** |
| [`OrderSummary`](#ordersummary) | Aggregated order statistics and revenue summaries | 0/8 — planned |
| [`Payment`](#payment) | Payments, payment methods, and booking payments to orders | 0/52 — planned |
| [`Pim`](#pim) | Product Information Management — modern `/rest/pim` item operations | **80/80** — full coverage |
| [`plentyMarketplace`](#plentymarketplace) | plentyMarkets plugin marketplace integration | 0/2 — planned |
| [`PluginMultilingualism`](#pluginmultilingualism) | Plugin translation strings and multilingual content | 0/5 — planned |
| [`Plugins`](#plugins) | Plugin installation, configuration, and lifecycle | 0/13 — planned |
| [`PluginSet`](#pluginset) | Plugin set management and deployment to clients | 0/26 — planned |
| [`Property`](#property) | Item and contact properties — property groups and values | 0/159 — planned |
| [`Returns`](#returns) | Return orders, return reasons, and return processing | 0/6 — planned |
| [`ShopBuilder`](#shopbuilder) | Webshop layout and drag-and-drop page builder configuration | 0/26 — planned |
| [`Stock`](#stock) | Item stock levels overview (legacy `/rest/stock` tree) | 0/1 — planned |
| [`StockManagement`](#stockmanagement) | Warehouses, storage locations, stock corrections/bookings, movements | **17/17** — full coverage |
| [`Sync`](#sync) | Data synchronisation jobs and field mapping configuration | 0/5 — planned |
| [`Tag`](#tag) | Tags for labelling orders, contacts, variations, etc. | 0/21 — planned |
| [`Ticket`](#ticket) | Support tickets and helpdesk case management | 0/8 — planned |
| [`TicketMessage`](#ticketmessage) | Messages and replies within support tickets | 0/4 — planned |
| [`Todo`](#todo) | Internal to-do tasks and user assignments | 0/5 — planned |
| [`User`](#user) | System users, user accounts, and preferences | 0/6 — planned |
| [`Warehouse`](#warehouse) | Warehouse configuration, storage locations, rack management | 0/37 — planned |
| [`Webstore`](#webstore) | Webshop settings, themes, plugins, and client configuration | 0/1 — planned |
| [`Wizard`](#wizard) | Setup wizards for guided first-time configuration | 0/16 — planned |

---

## Endpoint detail

### `Account`

4/151 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| POST | `/rest/account/login` | Login frontend user | planned | — |
| POST | `/rest/account/login/refresh` | Refresh access token | planned | — |
| POST | `/rest/account/logout` | Logout frontend user | planned | — |
| GET | `/rest/accounts` | List companies | planned | — |
| POST | `/rest/accounts` | Create company | planned | — |
| GET | `/rest/accounts/addresses` | Get addresses | planned | — |
| POST | `/rest/accounts/addresses` | Create address | planned | — |
| GET | `/rest/accounts/addresses/contact_relations` | List address contact relations | planned | — |
| POST | `/rest/accounts/addresses/contact_relations` | Create address contact relations | planned | — |
| PUT | `/rest/accounts/addresses/contact_relations` | Update address contact relations | planned | — |
| DELETE | `/rest/accounts/addresses/contact_relations/{addressContactRelationId}` | Delete address contact relation | planned | — |
| GET | `/rest/accounts/addresses/contact_relations/{addressContactRelationId}` | Get address contact relation | planned | — |
| GET | `/rest/accounts/addresses/option_types` | List address option types | planned | — |
| POST | `/rest/accounts/addresses/option_types` | Create address option type | planned | — |
| DELETE | `/rest/accounts/addresses/option_types/{optionTypeId}` | Delete address option type | planned | — |
| GET | `/rest/accounts/addresses/option_types/{optionTypeId}` | Get address option type | planned | — |
| PUT | `/rest/accounts/addresses/option_types/{optionTypeId}` | Update address option type | planned | — |
| DELETE | `/rest/accounts/addresses/options/{optionId}` | Delete address option by option ID | planned | — |
| GET | `/rest/accounts/addresses/options/{optionId}` | Get address option | planned | — |
| PUT | `/rest/accounts/addresses/options/{optionId}` | Update address option | planned | — |
| GET | `/rest/accounts/addresses/pos_relations` | List address POS relations | planned | — |
| POST | `/rest/accounts/addresses/pos_relations` | Create address POS relation | planned | — |
| DELETE | `/rest/accounts/addresses/pos_relations/{addressPosRelationId}` | Delete address POS relation | planned | — |
| GET | `/rest/accounts/addresses/pos_relations/{addressPosRelationId}` | Get address POS relation | planned | — |
| PUT | `/rest/accounts/addresses/pos_relations/{addressPosRelationId}` | Update address POS relation | planned | — |
| GET | `/rest/accounts/addresses/relation_types` | List address relation types | planned | — |
| GET | `/rest/accounts/addresses/relations/types/applications/{application}/{lang}` | List address relation types | planned | — |
| POST | `/rest/accounts/addresses/warehouse_relations` | Create address warehouse relation | planned | — |
| DELETE | `/rest/accounts/addresses/warehouse_relations/{relationId}` | Delete address warehouse relation | planned | — |
| PUT | `/rest/accounts/addresses/warehouse_relations/{relationId}` | Update address warehouse relation | planned | — |
| DELETE | `/rest/accounts/addresses/{addressId}` | Delete address | planned | — |
| GET | `/rest/accounts/addresses/{addressId}` | Get address | planned | — |
| PUT | `/rest/accounts/addresses/{addressId}` | Update address | planned | — |
| DELETE | `/rest/accounts/addresses/{addressId}/options` | Delete address option by addressId | planned | — |
| GET | `/rest/accounts/addresses/{addressId}/options` | List address options | planned | — |
| POST | `/rest/accounts/addresses/{addressId}/options` | Create address option | planned | — |
| PUT | `/rest/accounts/addresses/{addressId}/options` | Update address option by addressId | planned | — |
| GET | `/rest/accounts/addresses/{addressId}/related_data` | Get address data by addressId | planned | — |
| DELETE | `/rest/accounts/batchDelete` | Delete Batch of Companies | planned | — |
| POST | `/rest/accounts/contact_relations` | Create company contact relation | planned | — |
| DELETE | `/rest/accounts/contact_relations/{accountContactRelationId}` | Delete company contact relation | planned | — |
| GET | `/rest/accounts/contact_relations/{accountContactRelationId}` | Get company contact relation | planned | — |
| PUT | `/rest/accounts/contact_relations/{accountContactRelationId}/primary` | Updates an account contact relation isPrimary field | planned | — |
| GET | `/rest/accounts/contacts` | List contacts | **implemented** | `contacts.list` |
| POST | `/rest/accounts/contacts` | Create contact | **implemented** | `contacts.create` |
| POST | `/rest/accounts/contacts/banks` | Create bank account | planned | — |
| DELETE | `/rest/accounts/contacts/banks/{contactBankId}` | Delete bank account | planned | — |
| GET | `/rest/accounts/contacts/banks/{contactBankId}` | Get bank account | planned | — |
| PUT | `/rest/accounts/contacts/banks/{contactBankId}` | Update bank account | planned | — |
| PUT | `/rest/accounts/contacts/batch_update` | Batch Update | planned | — |
| GET | `/rest/accounts/contacts/classes` | List contact classes | planned | — |
| POST | `/rest/accounts/contacts/classes` | Creates a contact class | planned | — |
| GET | `/rest/accounts/contacts/classes/paginated` | List contact classes paginated | planned | — |
| DELETE | `/rest/accounts/contacts/classes/{contactClassId}` | Deletes a contact class | planned | — |
| GET | `/rest/accounts/contacts/classes/{contactClassId}` | Returns contact class model based on ID | planned | — |
| PUT | `/rest/accounts/contacts/classes/{contactClassId}` | Updates a contact class | planned | — |
| GET | `/rest/accounts/contacts/classesWithData` | List contact classes | planned | — |
| GET | `/rest/accounts/contacts/contact_events` | List contact events | planned | — |
| POST | `/rest/accounts/contacts/contact_events` | Create contact event | planned | — |
| GET | `/rest/accounts/contacts/contact_events/types/preview` | Get contact event types as a key/value array | planned | — |
| DELETE | `/rest/accounts/contacts/contact_events/{contactEventId}` | Delete contact event | planned | — |
| PUT | `/rest/accounts/contacts/contact_events/{contactEventId}` | Update contact event | planned | — |
| GET | `/rest/accounts/contacts/departments` | List contact departments | planned | — |
| POST | `/rest/accounts/contacts/departments` | Create contact department | planned | — |
| DELETE | `/rest/accounts/contacts/departments/{departmentId}` | Delete contact department | planned | — |
| GET | `/rest/accounts/contacts/departments/{departmentId}` | Get contact department | planned | — |
| PUT | `/rest/accounts/contacts/departments/{departmentId}` | Update contact department | planned | — |
| GET | `/rest/accounts/contacts/group_functions` | List all group function related data | planned | — |
| POST | `/rest/accounts/contacts/group_functions` | Apply selected group function options for given contact IDs | planned | — |
| GET | `/rest/accounts/contacts/option_sub_types` | List contact option sub-types | planned | — |
| POST | `/rest/accounts/contacts/option_sub_types` | Create contact option sub-type | planned | — |
| DELETE | `/rest/accounts/contacts/option_sub_types/{optionSubTypeId}` | Delete contact option sub-type | planned | — |
| GET | `/rest/accounts/contacts/option_sub_types/{optionSubTypeId}` | Get contact option sub-type | planned | — |
| PUT | `/rest/accounts/contacts/option_sub_types/{optionSubTypeId}` | Update contact option sub-type | planned | — |
| GET | `/rest/accounts/contacts/option_types` | List contact option types | planned | — |
| POST | `/rest/accounts/contacts/option_types` | Create contact option type | planned | — |
| DELETE | `/rest/accounts/contacts/option_types/{optionTypeId}` | Delete contact option type | planned | — |
| GET | `/rest/accounts/contacts/option_types/{optionTypeId}` | Get contact option type | planned | — |
| PUT | `/rest/accounts/contacts/option_types/{optionTypeId}` | Update contact option type | planned | — |
| DELETE | `/rest/accounts/contacts/options/{optionId}` | Delete contact option | planned | — |
| GET | `/rest/accounts/contacts/options/{optionId}` | Get contact option | planned | — |
| PUT | `/rest/accounts/contacts/options/{optionId}` | Update contact option | planned | — |
| GET | `/rest/accounts/contacts/positions` | List contact positions | planned | — |
| POST | `/rest/accounts/contacts/positions` | Create contact position | planned | — |
| DELETE | `/rest/accounts/contacts/positions/{positionId}` | Delete contact position | planned | — |
| GET | `/rest/accounts/contacts/positions/{positionId}` | Get contact position | planned | — |
| PUT | `/rest/accounts/contacts/positions/{positionId}` | Update contact position | planned | — |
| GET | `/rest/accounts/contacts/sales_representative_regions` | Get sales representative of region | planned | — |
| GET | `/rest/accounts/contacts/types` | List contact types | planned | — |
| POST | `/rest/accounts/contacts/types` | Create contact type | planned | — |
| DELETE | `/rest/accounts/contacts/types/{typeId}` | Delete contact type | planned | — |
| GET | `/rest/accounts/contacts/types/{typeId}` | Get contact type | planned | — |
| PUT | `/rest/accounts/contacts/types/{typeId}` | Update contact type | planned | — |
| DELETE | `/rest/accounts/contacts/{contactId}` | Delete contact | planned | — |
| GET | `/rest/accounts/contacts/{contactId}` | Get contact | **implemented** | `contacts.get` |
| PUT | `/rest/accounts/contacts/{contactId}` | Update contact | **implemented** | `contacts.update` |
| GET | `/rest/accounts/contacts/{contactId}/access_data/login_url` | Get login URL | planned | — |
| PUT | `/rest/accounts/contacts/{contactId}/access_data/new_password` | Send password link for contact | planned | — |
| PUT | `/rest/accounts/contacts/{contactId}/access_data/set_password` | Update password for contact | planned | — |
| PUT | `/rest/accounts/contacts/{contactId}/access_data/unblock_user` | Unblock contact | planned | — |
| POST | `/rest/accounts/contacts/{contactId}/accounts` | Create company for existing contact | planned | — |
| DELETE | `/rest/accounts/contacts/{contactId}/accounts/{accountId}` | Delete company of the contact | planned | — |
| GET | `/rest/accounts/contacts/{contactId}/accounts/{accountId}` | Get company of the contact | planned | — |
| PUT | `/rest/accounts/contacts/{contactId}/accounts/{accountId}` | Update company | planned | — |
| POST | `/rest/accounts/contacts/{contactId}/addresses` | Create address for existing contact | planned | — |
| GET | `/rest/accounts/contacts/{contactId}/addresses/primary` | Get primary or last created addresses of contact | planned | — |
| DELETE | `/rest/accounts/contacts/{contactId}/addresses/{addressId}` | Delete address of the contact | planned | — |
| PUT | `/rest/accounts/contacts/{contactId}/addresses/{addressId}` | Update address of the contact | planned | — |
| PUT | `/rest/accounts/contacts/{contactId}/addresses/{addressId}/types/{addressTypeId}/primary` | Set contact address per address type as primary address | planned | — |
| PUT | `/rest/accounts/contacts/{contactId}/addresses/{addressId}/types/{addressTypeId}/reset_primary` | Reset contact primary address | planned | — |
| GET | `/rest/accounts/contacts/{contactId}/addresses/{addressTypeId?}` | List addresses that are linked with contacts | planned | — |
| PUT | `/rest/accounts/contacts/{contactId}/anonymize` | Anonymize contact | planned | — |
| GET | `/rest/accounts/contacts/{contactId}/banks` | List bank accounts | planned | — |
| GET | `/rest/accounts/contacts/{contactId}/banksPaginated` | List bank accounts paginated | planned | — |
| GET | `/rest/accounts/contacts/{contactId}/contact_events` | List contact events by contact ID | planned | — |
| GET | `/rest/accounts/contacts/{contactId}/document` | Get storage object from contact documents | planned | — |
| POST | `/rest/accounts/contacts/{contactId}/document` | Upload document to contact directory | planned | — |
| POST | `/rest/accounts/contacts/{contactId}/document/link` | Upload document to contact directory | planned | — |
| PUT | `/rest/accounts/contacts/{contactId}/document/link/{documentId}` | Update an existing document link | planned | — |
| GET | `/rest/accounts/contacts/{contactId}/document/url` | Get temporary url for document | planned | — |
| DELETE | `/rest/accounts/contacts/{contactId}/documents` | Delete files from contact documents | planned | — |
| GET | `/rest/accounts/contacts/{contactId}/documents` | List documents of a contact | planned | — |
| DELETE | `/rest/accounts/contacts/{contactId}/options` | Delete contact option | planned | — |
| GET | `/rest/accounts/contacts/{contactId}/options` | List contact options | planned | — |
| POST | `/rest/accounts/contacts/{contactId}/options` | Create contact option | planned | — |
| PUT | `/rest/accounts/contacts/{contactId}/options` | Update contact option | planned | — |
| GET | `/rest/accounts/contacts/{contactId}/options/validate` | Validate contact option by given value | planned | — |
| GET | `/rest/accounts/contacts/{contactId}/related_data` | List contact related data | planned | — |
| GET | `/rest/accounts/contacts/{contactId}/sales_representative_regions` | List regions by contactId | planned | — |
| GET | `/rest/accounts/contacts/{contactId}/vcard` | Get vcard filestream of contact | planned | — |
| POST | `/rest/accounts/guests/convert` | Convert guest account into regular account | planned | — |
| GET | `/rest/accounts/jobs` | Get paginated list of jobs based on provided parameters | planned | — |
| POST | `/rest/accounts/jobs` | Create a job with given data | planned | — |
| DELETE | `/rest/accounts/jobs/{jobId}` | Delete a job by a given id | planned | — |
| GET | `/rest/accounts/jobs/{jobId}` | Get single job by id | planned | — |
| PUT | `/rest/accounts/jobs/{jobId}` | Update a job names with given data. The id of the job must be specified. | planned | — |
| DELETE | `/rest/accounts/sales_representative_regions/{salesRepresentativeRegionId}` | Delete region | planned | — |
| GET | `/rest/accounts/sales_representative_regions/{salesRepresentativeRegionId}` | Get region by ID | planned | — |
| PUT | `/rest/accounts/sales_representative_regions/{salesRepresentativeRegionId}` | Update region | planned | — |
| DELETE | `/rest/accounts/{accountId}` | Delete company | planned | — |
| GET | `/rest/accounts/{accountId}` | Get company | planned | — |
| PUT | `/rest/accounts/{accountId}` | Update company | planned | — |
| GET | `/rest/accounts/{accountId}/contacts` | List contacts | planned | — |
| GET | `/rest/accounts/{accountId}/contacts/{contactId}/sales_representative_regions` | Get region by contactId and accountId | planned | — |
| POST | `/rest/accounts/{accountId}/contacts/{contactId}/sales_representative_regions` | Create region for sales representative | planned | — |
| POST | `/rest/orders/addresses` | Create address for existing order | planned | — |
| PUT | `/rest/orders/{orderId}/addresses/{addressId}/{relationTypeId}` | Update an address for an existing order. | planned | — |
| GET | `/rest/orders/{orderId}/addresses/{relationTypeId?}` | List order addresses | planned | — |
| POST | `/rest/orders/{orderId}/addresses/{relationTypeId}` | Create an address for an existing order. | planned | — |
| POST | `/rest/stockmanagement/warehouses/addresses` | Create address for existing warehouse | planned | — |
| GET | `/rest/stockmanagement/warehouses/{warehouseId}/addresses/{relationTypeId?}` | List warehouse addresses | planned | — |

### `Accounting`

0/35 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| POST | `/rest/accounting/locations` | Create an accounting location | planned | — |
| GET | `/rest/accounting/locations/existing_accounts` | Get all unique posting accounts | planned | — |
| GET | `/rest/accounting/locations/posting_accounts` | Get all posting accounts | planned | — |
| POST | `/rest/accounting/locations/posting_accounts` | Save posting accounts | planned | — |
| DELETE | `/rest/accounting/locations/posting_accounts/{id}` | Delete a posting account | planned | — |
| GET | `/rest/accounting/locations/posting_accounts/{id}` | Get posting account | planned | — |
| GET | `/rest/accounting/locations/revenue_account_configurations` | List revenue account configurations | planned | — |
| DELETE | `/rest/accounting/locations/{locationId}` | Delete an accounting location | planned | — |
| GET | `/rest/accounting/locations/{locationId}` | Get an accounting location | planned | — |
| PUT | `/rest/accounting/locations/{locationId}` | Update an accounting location | planned | — |
| GET | `/rest/accounting/locations/{locationId}/countries/{countryId}/revenue_accounts` | Get the revenue account configuration of a country | planned | — |
| GET | `/rest/accounting/locations/{locationId}/debtor_account_configurations` | Get debtor account configuration of an accounting location | planned | — |
| PUT | `/rest/accounting/locations/{locationId}/debtor_account_configurations` | Update debtor account configuration of an accounting location | planned | — |
| GET | `/rest/accounting/locations/{locationId}/debtor_accounts/{mode}` | Lists the debtor accounts by mode. | planned | — |
| GET | `/rest/accounting/locations/{locationId}/posting_accounts` | Get posting accounts by locationId | planned | — |
| GET | `/rest/accounting/locations/{locationId}/posting_key_configurations` | Get a posting key configuration of an accounting location | planned | — |
| PUT | `/rest/accounting/locations/{locationId}/posting_key_configurations` | Update a posting key configuration of an accounting location | planned | — |
| GET | `/rest/accounting/locations/{locationId}/revenue_account_configurations` | Get the revenue account configuration of an accounting location | planned | — |
| PUT | `/rest/accounting/locations/{locationId}/revenue_account_configurations` | Update the revenue account configuration of an accounting location | planned | — |
| GET | `/rest/accounting/locations/{locationId}/settings` | Get accounting location settings | planned | — |
| PUT | `/rest/accounting/locations/{locationId}/settings` | Update accounting location settings | planned | — |
| GET | `/rest/accounting/locations/{locationId}/{type}/posting_accounts` | Get posting accounts by locationId and type | planned | — |
| GET | `/rest/accounting/locations/{webstoreId}/{countryId}/posting_accounts` | Get posting accounts by country and webstore | planned | — |
| GET | `/rest/accounting/stores/locations` | List accounting locations | planned | — |
| GET | `/rest/accounting/stores/{plentyId}/locations` | List accounting locations of a client | planned | — |
| GET | `/rest/stores/{plentyId}/locations` | Get the ID of an accounting location of a country | planned | — |
| GET | `/rest/vat` | List VAT configurations. | planned | — |
| POST | `/rest/vat` | Create a VAT configuration | planned | — |
| GET | `/rest/vat/locations/{locationId}` | List VAT configurations of an accounting location | planned | — |
| GET | `/rest/vat/locations/{locationId}/countries/{countryId}` | List VAT configurations for one country of delivery | planned | — |
| GET | `/rest/vat/locations/{locationId}/countries/{countryId}/date/{date}` | Get a VAT configuration for a country in a location. | planned | — |
| GET | `/rest/vat/standard` | Get a VAT configuration for the standard accounting location of a client | planned | — |
| DELETE | `/rest/vat/{vatId}` | Delete a VAT configuration | planned | — |
| GET | `/rest/vat/{vatId}` | Get a VAT configuration by id | planned | — |
| PUT | `/rest/vat/{vatId}` | Update a VAT configuration | planned | — |

### `AddressDesign`

0/9 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/address_layout` | List all layouts with their contents | planned | — |
| POST | `/rest/address_layout` | Create new layout | planned | — |
| GET | `/rest/address_layout/country/{countryId}` | Get layout by country id | planned | — |
| GET | `/rest/address_layout/default` | Get default layout | planned | — |
| GET | `/rest/address_layout/used_countries/{uuid?}` | List countries used in other layouts | planned | — |
| DELETE | `/rest/address_layout/{uuid}` | Delete layout | planned | — |
| GET | `/rest/address_layout/{uuid}` | Get layout | planned | — |
| PUT | `/rest/address_layout/{uuid}` | Update layout | planned | — |
| GET | `/rest/address_layout_fields` | List all available fields | planned | — |

### `AuditLog`

0/8 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/audit-log/archive` | Get available audit log archives. | planned | — |
| POST | `/rest/audit-log/archive/{key}/restore` | Restore an audit log archive | planned | — |
| GET | `/rest/audit-log/archive/{key}/signed-url` | Get the download url for an restored audit log archive | planned | — |
| GET | `/rest/audit-log/entities` | Get available audit log entities. | planned | — |
| GET | `/rest/audit-log/files` | Get available audit log entities. | planned | — |
| GET | `/rest/audit-log/files/{key}/signed-url` | Get the download url for an restored audit log file | planned | — |
| GET | `/rest/audit-log/system-config` | Get audit log system config | planned | — |
| POST | `/rest/audit-log/system-config` | Write the system config | planned | — |

### `Authentication`

0/9 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| POST | `/rest/check_password` | Check password | planned | — |
| POST | `/rest/check_pin` | Check given pin | planned | — |
| POST | `/rest/login` | Login by backend user | internal | `_session.py` (`PlentyClient._login`) |
| POST | `/rest/login/refresh` | Refresh access token | planned | — |
| POST | `/rest/logout` | Logout user | planned | — |
| POST | `/rest/quick_login` | Quick login user | planned | — |
| GET | `/rest/session_limits` | Get session limits | planned | — |
| GET | `/rest/user` | Get user | planned | — |
| POST | `/rest/users/{id}/reset_failed_attempts` | Reset failed authentication attempts | planned | — |

### `Authorization`

0/3 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/authorized_user` | Get authorized user | planned | — |
| GET | `/rest/user/authorized_user_with_ui_config` | Get authorized user with UiConfig | planned | — |
| GET | `/rest/users/me` | Get authorized user | planned | — |

### `Basket`

0/4 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/basket` | Get basket | planned | — |
| GET | `/rest/basket/items` | List basket items | planned | — |
| POST | `/rest/basket/items` | Add item to basket | planned | — |
| GET | `/rest/basket/items/{id}` | Find a basket item by it's ID | planned | — |

### `Batch`

0/1 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/batch` | Make batch requests | planned | — |

### `BI`

0/31 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/bi/key-figures` | Return list of key figure classes | planned | — |
| GET | `/rest/bi/key-figures/config` | Returns all key figure configs | planned | — |
| POST | `/rest/bi/key-figures/config` | Add a key figure configuration | planned | — |
| POST | `/rest/bi/key-figures/config/template` | Generate key figure config from template class | planned | — |
| GET | `/rest/bi/key-figures/config/templates` | Get key figure templates | planned | — |
| DELETE | `/rest/bi/key-figures/config/{keyFigureConfigId}` | Delete key figure configuration | planned | — |
| GET | `/rest/bi/key-figures/config/{keyFigureConfigId}` | Get key figure config | planned | — |
| PUT | `/rest/bi/key-figures/config/{keyFigureConfigId}` | Update key figure configuration | planned | — |
| DELETE | `/rest/bi/key-figures/configs` | Delete multiple key figure configurations | planned | — |
| GET | `/rest/bi/key-figures/details/{keyFigureName}` | Return key figure calculation details | planned | — |
| GET | `/rest/bi/key-figures/dimensions/{keyFigure}` | Return key figure dimensions and dimension values | planned | — |
| POST | `/rest/bi/key-figures/global-filters` | Return global filters by given key figure identifiers param: identifiers | planned | — |
| POST | `/rest/bi/key-figures/global-filters/values` | Return global filter values by given criteria identifiers param: identifiers | planned | — |
| GET | `/rest/bi/key-figures/raw-data/{keyFigureConfigId}` | Return filtered raw data for given key figure | planned | — |
| POST | `/rest/bi/key-figures/raw-data/{keyFigureConfigId}` | Return filtered raw data for given key figure | planned | — |
| POST | `/rest/bi/key-figures/raw-data/{keyFigureConfigId}/export-spreadsheet` | Export raw data of a given key figure to a spreadsheet (google, microsoft) | planned | — |
| POST | `/rest/bi/key-figures/recalculate` | Recalculates one or more raw data based key figures by key figure config ids | planned | — |
| POST | `/rest/bi/key-figures/results` | Search for key figure calculation results | planned | — |
| GET | `/rest/bi/order-types` | Get order types in string format | planned | — |
| GET | `/rest/bi/raw-data` | Get list of raw data files. | planned | — |
| GET | `/rest/bi/raw-data/config` | Returns list of all saved configurations | planned | — |
| PUT | `/rest/bi/raw-data/config` | Resets all saved raw data configurations with given data | planned | — |
| GET | `/rest/bi/raw-data/creators` | Get list of all raw data creators | planned | — |
| GET | `/rest/bi/raw-data/creators-configs` | Return a list of raw data creators with their configurations | planned | — |
| GET | `/rest/bi/raw-data/file` | Get a raw data file from the storage | planned | — |
| DELETE | `/rest/bi/raw-data/{dataName}` | Deletes RawData\Models that are deletable | planned | — |
| GET | `/rest/reports/raw-data` | Get list of raw data files. | planned | — |
| PUT | `/rest/reports/raw-data/config` | Resets all saved raw data configurations with given data | planned | — |
| GET | `/rest/reports/raw-data/creators` | Get list of all raw data creators | planned | — |
| GET | `/rest/reports/raw-data/creators-configs` | Return a list of raw data creators with their configurations | planned | — |
| GET | `/rest/reports/raw-data/file` | Get a raw data file from the storage | planned | — |

### `Blog`

0/5 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| POST | `/rest/blogs/post` | Create a blog post | planned | — |
| DELETE | `/rest/blogs/post/{postId}` | Delete a blog post | planned | — |
| GET | `/rest/blogs/post/{postId}` | Get a blog post | planned | — |
| PUT | `/rest/blogs/post/{postId}` | Update a blog post | planned | — |
| GET | `/rest/blogs/posts` | List blog posts | planned | — |

### `Board`

0/16 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/boards/{boardId}/columns` | List all columns of a given board | planned | — |
| POST | `/rest/boards/{boardId}/columns` | Create column and assign it to a board | planned | — |
| DELETE | `/rest/boards/{boardId}/columns/{columnId}` | Delete column | planned | — |
| POST | `/rest/boards/{boardId}/columns/{columnId}` | Copy column | planned | — |
| PUT | `/rest/boards/{boardId}/columns/{columnId}` | Update column | planned | — |
| PUT | `/rest/boards/{boardId}/columns/{columnId}/position` | Update position of of a column | planned | — |
| GET | `/rest/boards/{boardId}/columns/{columnId}/tasks` | List all task of a column | planned | — |
| POST | `/rest/boards/{boardId}/columns/{columnId}/tasks` | Create task in specific column | planned | — |
| DELETE | `/rest/boards/{boardId}/columns/{columnId}/tasks/{taskId}` | Delete task | planned | — |
| GET | `/rest/boards/{boardId}/columns/{columnId}/tasks/{taskId}` | Get task by ID | planned | — |
| POST | `/rest/boards/{boardId}/columns/{columnId}/tasks/{taskId}` | Copy task | planned | — |
| PUT | `/rest/boards/{boardId}/columns/{columnId}/tasks/{taskId}` | Update task | planned | — |
| PUT | `/rest/boards/{boardId}/columns/{columnId}/tasks/{taskId}/position` | Update task position | planned | — |
| POST | `/rest/boards/{boardId}/columns/{columnId}/tasks/{taskId}/references` | Create reference | planned | — |
| DELETE | `/rest/boards/{boardId}/columns/{columnId}/tasks/{taskId}/references/{referenceId}` | Delete reference from a given task | planned | — |
| GET | `/rest/boards/{boardId}/columns/{columnId}/tasks/{taskId}/references/{referenceType}/{referenceKey}` | Check reference key | planned | — |

### `Boards`

0/6 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/boards` | List all boards | planned | — |
| POST | `/rest/boards` | Create new board | planned | — |
| DELETE | `/rest/boards/{boardId}` | Delete board | planned | — |
| GET | `/rest/boards/{boardId}` | Get board by ID | planned | — |
| POST | `/rest/boards/{boardId}` | Copy board | planned | — |
| PUT | `/rest/boards/{boardId}` | Update board | planned | — |

### `Catalog`

0/33 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/catalogs/catalogs` | Gets a list of Catalogs | planned | — |
| POST | `/rest/catalogs/catalogs` | Create Catalog | planned | — |
| POST | `/rest/catalogs/catalogs/activate/{id}` | Activate or deactivate Catalog | planned | — |
| GET | `/rest/catalogs/catalogs/archive` | Get archive | planned | — |
| POST | `/rest/catalogs/catalogs/archive/{id}/restore` | Restore archived Catalog | planned | — |
| PUT | `/rest/catalogs/catalogs/copy` | Copy Catalog | planned | — |
| POST | `/rest/catalogs/catalogs/import` | Import a catalog. | planned | — |
| POST | `/rest/catalogs/catalogs/migrate` | Migrate Catalogs | planned | — |
| GET | `/rest/catalogs/catalogs/schedule/days` | Return available schedule days list | planned | — |
| GET | `/rest/catalogs/catalogs/token` | Generate token | planned | — |
| PUT | `/rest/catalogs/catalogs/{catalogId}/copy` | Copy Catalog format | planned | — |
| DELETE | `/rest/catalogs/catalogs/{id}` | Delete Catalog | planned | — |
| GET | `/rest/catalogs/catalogs/{id}` | Get Catalog | planned | — |
| PUT | `/rest/catalogs/catalogs/{id}` | Update Catalog | planned | — |
| GET | `/rest/catalogs/catalogs/{id}/content` | Get Catalog content | planned | — |
| PUT | `/rest/catalogs/catalogs/{id}/content` | Update Catalog content | planned | — |
| GET | `/rest/catalogs/catalogs/{id}/export` | Export a catalog. | planned | — |
| GET | `/rest/catalogs/catalogs/{id}/preview` | Get preview catalog | planned | — |
| GET | `/rest/catalogs/catalogs/{id}/preview/vdi` | Get preview VDI catalog | planned | — |
| GET | `/rest/catalogs/catalogs/{id}/url/private` | Build private download url | planned | — |
| GET | `/rest/catalogs/catalogs/{id}/url/public` | Build public download url | planned | — |
| GET | `/rest/catalogs/catalogs/{id}/versions` | Lists Catalog versions | planned | — |
| GET | `/rest/catalogs/catalogs/{id}/versions/{versionId}` | Gets Catalog by version | planned | — |
| POST | `/rest/catalogs/catalogs/{id}/versions/{versionId}/restore` | Restore version of Catalog | planned | — |
| POST | `/rest/catalogs/connection/check/{protocol}` | Check the connection to FTP, FTPS, SFTP | planned | — |
| GET | `/rest/catalogs/statuses` | Get a list of Catalog statuses | planned | — |
| GET | `/rest/catalogs/statuses/{id}` | Get Catalog status | planned | — |
| GET | `/rest/catalogs/statuses/{id}/data` | Get status data | planned | — |
| GET | `/rest/catalogs/statuses/{id}/histories` | List status histories | planned | — |
| GET | `/rest/catalogs/statuses/{id}/histories/{filename}` | Get a single status history file | planned | — |
| GET | `/rest/catalogs/statuses/{id}/logs` | List status logs | planned | — |
| GET | `/rest/catalogs/statuses/{id}/performances` | List status performances | planned | — |
| POST | `/rest/catalogs/statuses/{statusId}/cancel` | Cancel export runs | planned | — |

### `Category`

0/13 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/categories` | List categories | planned | — |
| POST | `/rest/categories` | Create new categories | planned | — |
| PUT | `/rest/categories` | Update categories | planned | — |
| DELETE | `/rest/categories/{id}` | Deletes a category | planned | — |
| GET | `/rest/categories/{id}` | Get a category | planned | — |
| PUT | `/rest/categories/{id}` | Updates one category | planned | — |
| DELETE | `/rest/categories/{id}/clients` | Deactivate availability for clients | planned | — |
| DELETE | `/rest/categories/{id}/details` | Delete category details for the specified languages | planned | — |
| DELETE | `/rest/categories/{id}/templates` | Delete a category template | planned | — |
| GET | `/rest/categories/{id}/templates` | Get a category template | planned | — |
| PUT | `/rest/categories/{id}/templates` | Update a category template | planned | — |
| GET | `/rest/category_branches` | Get category trees | planned | — |
| GET | `/rest/category_branches/{id}` | Get category tree | planned | — |

### `Cloud`

0/21 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| DELETE | `/rest/storage/frontend/file` | Delete object from frontend storage | planned | — |
| GET | `/rest/storage/frontend/file` | Get file information | planned | — |
| POST | `/rest/storage/frontend/file` | Upload a single file to frontend storage. | planned | — |
| PUT | `/rest/storage/frontend/file` | Upload a single file to frontend storage. | planned | — |
| GET | `/rest/storage/frontend/file/metadata` | Get metadata for storage object | planned | — |
| POST | `/rest/storage/frontend/file/metadata` | Update metadata of storage object | planned | — |
| DELETE | `/rest/storage/frontend/files` | Delete files from frontend storage. | planned | — |
| GET | `/rest/storage/frontend/files` | List frontend storage files | planned | — |
| GET | `/rest/storage/frontend/object-url` | Get the URL for a layout document | planned | — |
| DELETE | `/rest/storage/layout` | Delete layout documents | planned | — |
| POST | `/rest/storage/layout` | Upload a layout document | planned | — |
| GET | `/rest/storage/layout/list` | List layout documents | planned | — |
| GET | `/rest/storage/layout/object-url` | Get the URL for a layout document | planned | — |
| GET | `/rest/storage/order-properties/object-url` | Get the URL for a order property file | planned | — |
| DELETE | `/rest/storage/plugins/inbox` | Delete files from the inbox | planned | — |
| POST | `/rest/storage/plugins/inbox` | Upload a file to the inbox | planned | — |
| POST | `/rest/storage/plugins/inbox/commit` | Commit plugin changes | planned | — |
| GET | `/rest/storage/plugins/inbox/list` | List files from the inbox | planned | — |
| GET | `/rest/storage/plugins/inbox/object-url` | Get the content of a file from the inbox | planned | — |
| GET | `/rest/system/cloud/metrics` | Get cloud metrics | planned | — |
| GET | `/rest/system/metrics/{plentyId}/{date}` | Get System metrics | planned | — |

### `Comment`

0/5 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| POST | `/rest/comments` | Create a comment | planned | — |
| DELETE | `/rest/comments/{commentId}` | Delete a comment | planned | — |
| GET | `/rest/comments/{commentId}` | Get a comment | planned | — |
| PUT | `/rest/comments/{commentId}` | Update a comment | planned | — |
| GET | `/rest/comments/{referenceType}/{referenceValue}` | List comments | planned | — |

### `Configuration`

0/5 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/plugins/plugin_sets/{pluginSetId}/configurations/export` | Exports a configuration file | planned | — |
| POST | `/rest/plugins/plugin_sets/{pluginSetId}/configurations/import` | Imports a configuration file | planned | — |
| GET | `/rest/plugins/{pluginId}/plugin_sets/{pluginSetId}/configuration_layout` | Get configuration file | planned | — |
| GET | `/rest/plugins/{pluginId}/plugin_sets/{pluginSetId}/configurations` | List configurations | planned | — |
| PUT | `/rest/plugins/{pluginId}/plugin_sets/{pluginSetId}/configurations` | Save configuration file | planned | — |

### `Document`

0/44 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/categories/{categoryId}/documents` | List documents of a category | planned | — |
| POST | `/rest/categories/{categoryId}/documents` | Upload category documents | planned | — |
| GET | `/rest/categories/{categoryId}/documents/downloads` | Download category documents | planned | — |
| DELETE | `/rest/categories/{categoryId}/documents/{documentId}` | Delete a category document. | planned | — |
| POST | `/rest/documents/incoming_items_receipt/generate` | Generate a document of an "stockIntake". | planned | — |
| POST | `/rest/documents/incoming_items_receipt/generate/preview` | Generates a preview of the "incoming items receipt". | planned | — |
| POST | `/rest/documents/preview/generate/{previewType}` | Generate a preview of a document | planned | — |
| GET | `/rest/documents/preview/{documentHash}` | Download the content of a preview document | planned | — |
| GET | `/rest/documents/{documentId}` | Download the content of a document | planned | — |
| GET | `/rest/documents/{documentId}/status` | Get status of a document | planned | — |
| GET | `/rest/orders/documents` | List order documents | planned | — |
| GET | `/rest/orders/documents/downloads/as_zip` | Download documents | planned | — |
| GET | `/rest/orders/documents/downloads/{type}` | Download documents of a document type | planned | — |
| GET | `/rest/orders/documents/find` | List documents | planned | — |
| GET | `/rest/orders/documents/{documentId}` | Get an order document. | planned | — |
| GET | `/rest/orders/documents/{type}` | List documents of a type | planned | — |
| POST | `/rest/orders/{orderId}/documents/correction_document/generate` | Generate adjustment form of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/credit_note/generate` | Generate credit note of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/delivery_note/generate` | Generate delivery note of an order | planned | — |
| GET | `/rest/orders/{orderId}/documents/downloads/{type?}` | Download documents of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/dunning_letter/generate` | Generate dunning letter of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/invoice/generate` | Generate invoice of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/multi_credit_note/generate` | Generate multi credit note of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/multi_invoice/generate` | Generate multi-invoice of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/offer/generate` | Generate offer document of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/order_confirmation/generate` | Generate order confirmation of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/order_custom/generate` | Generate order custom document of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/pickup_delivery/generate` | Generate pick-up delivery note of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/po_delivery_note/generate` | Generate purchase order (PO) delivery note of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/pro_forma_invoice/generate` | Generate pro forma invoice of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/reorder/generate` | Generate reorder document of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/repair_bill/generate` | Generate repair slip of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/return_note/generate` | Generate return slip of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/reversal_document/generate` | Generate reversal document of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/reversal_dunning_letter/generate` | Generate dunning letter reversal document of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/reversal_refund/generate` | Generate refund reversal document of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/success_confirmation/generate` | Generate success confirmation of an order | planned | — |
| DELETE | `/rest/orders/{orderId}/documents/{documentId}` | Delete document of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/{documentId}/archive` | Archive document of an order | planned | — |
| GET | `/rest/orders/{orderId}/documents/{type?}` | List documents of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/{type}` | Upload order documents | planned | — |
| GET | `/rest/orders/{orderId}/documents/{type}/current` | Get current invoice or credit note of an order | planned | — |
| POST | `/rest/orders/{orderId}/documents/{type}/generate` | Generate document of an order | planned | — |
| GET | `/rest/orders/{orderId}/documents/{type}/recent` | Get most recent document of an order | planned | — |

### `ElasticSync`

0/75 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/elastic-sync/mapping/csv-rows/{syncId}` | Get the csv rows. | planned | — |
| GET | `/rest/elastic-sync/mapping/fields/{syncType}` | Get the plenty fields value map for a particular sync type. | planned | — |
| GET | `/rest/elastic-sync/mapping/filter/labels` | Get the label list for mapping filtration. | planned | — |
| GET | `/rest/elastic-sync/mapping/map/csv-columns/{syncId}` | Get the csv columns of a sync. | planned | — |
| GET | `/rest/elastic-sync/mapping/map/tree` | Get the mapping values tree. | planned | — |
| GET | `/rest/elastic-sync/mapping/model/{syncType}` | Get the model key to field value key. | planned | — |
| GET | `/rest/elastic-sync/mapping/values/{syncType}` | Get the mapping values. | planned | — |
| GET | `/rest/elastic-sync/mapping/variation` | Get a list with variation matches. | planned | — |
| POST | `/rest/elastic-sync/sync` | Create a sync. | planned | — |
| PUT | `/rest/elastic-sync/sync/change-csv` | Update the Csv of a Sync. | planned | — |
| POST | `/rest/elastic-sync/sync/import` | Save the CSV on S3. | planned | — |
| POST | `/rest/elastic-sync/sync/import-different` | Import the sync with different plentyId. | planned | — |
| POST | `/rest/elastic-sync/sync/import/file/public-url` | Save the CSV on S3. | planned | — |
| POST | `/rest/elastic-sync/sync/import/file/public-url/different` | Import the sync with different plentyId. | planned | — |
| GET | `/rest/elastic-sync/sync/intervals` | Get list of sync intervals. | planned | — |
| DELETE | `/rest/elastic-sync/sync/mapping/filter/{filterId}` | Delete a sync mapping. | planned | — |
| GET | `/rest/elastic-sync/sync/mapping/filter/{filterId}` | Get a sync mapping. | planned | — |
| PUT | `/rest/elastic-sync/sync/mapping/filter/{filterId}` | Update a sync mapping filter. | planned | — |
| DELETE | `/rest/elastic-sync/sync/mapping/row/{rowId}` | Delete a sync mapping row. | planned | — |
| GET | `/rest/elastic-sync/sync/mapping/row/{rowId}` | Get a sync mapping row. | planned | — |
| PUT | `/rest/elastic-sync/sync/mapping/row/{rowId}` | Update a sync mapping row. | planned | — |
| DELETE | `/rest/elastic-sync/sync/mapping/{mappingId}` | Delete a sync mapping. | planned | — |
| GET | `/rest/elastic-sync/sync/mapping/{mappingId}` | Get a sync mapping. | planned | — |
| PUT | `/rest/elastic-sync/sync/mapping/{mappingId}` | Update a sync mapping. | planned | — |
| POST | `/rest/elastic-sync/sync/mapping/{mappingId}/filter` | Create a sync mapping filter. | planned | — |
| GET | `/rest/elastic-sync/sync/mapping/{mappingId}/filters` | List sync mappings. | planned | — |
| POST | `/rest/elastic-sync/sync/mapping/{mappingId}/filters` | Create sync mapping filters. | planned | — |
| PUT | `/rest/elastic-sync/sync/mapping/{mappingId}/filters` | Update sync mapping filters. | planned | — |
| POST | `/rest/elastic-sync/sync/mapping/{mappingId}/row` | Create a sync mapping row. | planned | — |
| GET | `/rest/elastic-sync/sync/mapping/{mappingId}/rows` | List sync mapping rows. | planned | — |
| POST | `/rest/elastic-sync/sync/mapping/{mappingId}/rows` | Create sync mapping rows. | planned | — |
| PUT | `/rest/elastic-sync/sync/mapping/{mappingId}/rows` | Update sync mapping rows. | planned | — |
| DELETE | `/rest/elastic-sync/sync/mappings` | Delete one or more mappings. | planned | — |
| POST | `/rest/elastic-sync/sync/mappings/copy` | Copy one or more mappings. | planned | — |
| GET | `/rest/elastic-sync/sync/matching/decimals` | Get list of decimals. | planned | — |
| DELETE | `/rest/elastic-sync/sync/matching/{matchingId}` | Delete a sync matching. | planned | — |
| GET | `/rest/elastic-sync/sync/matching/{matchingId}` | Get a sync matching. | planned | — |
| PUT | `/rest/elastic-sync/sync/matching/{matchingId}` | Update a sync matching. | planned | — |
| DELETE | `/rest/elastic-sync/sync/option/{optionId}` | Delete a sync. | planned | — |
| GET | `/rest/elastic-sync/sync/option/{optionId}` | Get a sync. | planned | — |
| PUT | `/rest/elastic-sync/sync/option/{optionId}` | Update a sync option. | planned | — |
| GET | `/rest/elastic-sync/sync/report/{id}` | Get Log by ID | planned | — |
| GET | `/rest/elastic-sync/sync/reports` | Check Report Log. | planned | — |
| GET | `/rest/elastic-sync/sync/reports/availability` | Check Report Log. | planned | — |
| GET | `/rest/elastic-sync/sync/reset-cache` | Reset the cache. | planned | — |
| GET | `/rest/elastic-sync/sync/schedule/times` | Get schedule times. | planned | — |
| GET | `/rest/elastic-sync/sync/status` | Get syncs status. | planned | — |
| GET | `/rest/elastic-sync/sync/types` | Get list of sync types. | planned | — |
| POST | `/rest/elastic-sync/sync/{statusId}/live/processing/{syncId}/{page}` | Import a page for Live Import | planned | — |
| POST | `/rest/elastic-sync/sync/{statusId}/live/queueing` | Get the list of jobs for Live Import | planned | — |
| DELETE | `/rest/elastic-sync/sync/{syncId}` | Delete a sync. | planned | — |
| GET | `/rest/elastic-sync/sync/{syncId}` | Get a sync. | planned | — |
| PUT | `/rest/elastic-sync/sync/{syncId}` | Update a sync. | planned | — |
| POST | `/rest/elastic-sync/sync/{syncId}/live/initiate` | Initiate + queue live import | planned | — |
| POST | `/rest/elastic-sync/sync/{syncId}/mapping` | Create a sync mapping. | planned | — |
| GET | `/rest/elastic-sync/sync/{syncId}/mappings` | List sync mappings. | planned | — |
| GET | `/rest/elastic-sync/sync/{syncId}/matches` | List sync matches. | planned | — |
| POST | `/rest/elastic-sync/sync/{syncId}/matches` | Create sync matches. | planned | — |
| PUT | `/rest/elastic-sync/sync/{syncId}/matches` | Update sync matches. | planned | — |
| POST | `/rest/elastic-sync/sync/{syncId}/matching` | Create a sync matching. | planned | — |
| GET | `/rest/elastic-sync/sync/{syncId}/matching/entity` | Get an entity. | planned | — |
| POST | `/rest/elastic-sync/sync/{syncId}/option` | Create a sync option. | planned | — |
| GET | `/rest/elastic-sync/sync/{syncId}/options` | List syncs. | planned | — |
| POST | `/rest/elastic-sync/sync/{syncId}/options` | Create sync options. | planned | — |
| PUT | `/rest/elastic-sync/sync/{syncId}/options` | Update sync options. | planned | — |
| GET | `/rest/elastic-sync/sync/{syncId}/preview-computed` | Get computed preview of mapped targets. | planned | — |
| GET | `/rest/elastic-sync/sync/{syncId}/preview-values` | Get preview of csv values. | planned | — |
| POST | `/rest/elastic-sync/sync/{syncId}/run` | Execute the run procedure. | planned | — |
| GET | `/rest/elastic-sync/sync/{syncId}/source-preview` | Preview the syncs. | planned | — |
| GET | `/rest/elastic-sync/sync/{syncType}/matching/fields` | Get a list of all mappings for a particular sync type. | planned | — |
| DELETE | `/rest/elastic-sync/syncs` | Delete syncs. | planned | — |
| GET | `/rest/elastic-sync/syncs` | Get all Syncs | planned | — |
| POST | `/rest/elastic-sync/syncs/copy` | Copy the syncs. | planned | — |
| POST | `/rest/elastic-sync/syncs/export` | Export the syncs. | planned | — |
| GET | `/rest/elastic-sync/syncs/export/{syncId}` | Export the sync. | planned | — |

### `Export`

0/6 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/export/{exportKey}` | Export an elastic export. | planned | — |
| GET | `/export/{exportKey}/{token}` | Export an elastic export. | planned | — |
| GET | `/rest/exports/format_keys` | Get format keys | planned | — |
| GET | `/rest/exports/format_keys/{type}` | Get format keys | planned | — |
| GET | `/rest/exports/generate_token` | Generate a token | planned | — |
| GET | `/rest/orders/shipping/export_documents/{orderId}` | List export documents | planned | — |

### `ExportSettings`

0/6 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/exports` | List elastic exports | planned | — |
| POST | `/rest/exports` | Create an export | planned | — |
| DELETE | `/rest/exports/{exportId}` | Delete export | planned | — |
| GET | `/rest/exports/{exportId}` | Get export | planned | — |
| PUT | `/rest/exports/{exportId}` | Update an export | planned | — |
| DELETE | `/rest/exports/{exportId}/filters/{key}` | Delete filter from the export | planned | — |

### `Feedback`

0/17 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| POST | `/rest/feedbacks/comment` | Create a feedback comment | planned | — |
| DELETE | `/rest/feedbacks/comment/{commentId}` | Delete a feedback comment | planned | — |
| GET | `/rest/feedbacks/comment/{commentId}` | Get a feedback comment | planned | — |
| GET | `/rest/feedbacks/comments` | List feedback comments | planned | — |
| DELETE | `/rest/feedbacks/delete_feedbacks/{feedbackIds}` | Delete multiple feedbacks | planned | — |
| POST | `/rest/feedbacks/feedback` | Create a feedback | planned | — |
| GET | `/rest/feedbacks/feedback/replies/{feedbackId}` | List feedback replies | planned | — |
| DELETE | `/rest/feedbacks/feedback/{feedbackId}` | Delete a feedback | planned | — |
| GET | `/rest/feedbacks/feedback/{feedbackId}` | Get a feedback | planned | — |
| PUT | `/rest/feedbacks/feedback/{feedbackId}` | Update a feedback | planned | — |
| GET | `/rest/feedbacks/feedbacks` | List feedbacks | planned | — |
| PUT | `/rest/feedbacks/feedbacks_visibility` | Update the visibility of multiple feedbacks | planned | — |
| POST | `/rest/feedbacks/migrate` | Migrate legacy feedbacks | planned | — |
| POST | `/rest/feedbacks/rating` | Create a feedback rating | planned | — |
| DELETE | `/rest/feedbacks/rating/{ratingId}` | Delete a feedback rating | planned | — |
| GET | `/rest/feedbacks/rating/{ratingId}` | Get a feedback rating | planned | — |
| GET | `/rest/feedbacks/ratings` | List feedback ratings | planned | — |

### `Fulfillment`

0/10 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/fulfillment/picklist` | Get all pick lists | planned | — |
| GET | `/rest/fulfillment/picklist/picking_order_item` | Get all pick list items | planned | — |
| GET | `/rest/fulfillment/picklist/picking_order_item/{pickingOrderItemId}` | Get pick list item | planned | — |
| POST | `/rest/fulfillment/picklist/picking_order_item/{pickingOrderItemId}/status` | Set state of a pick list item | planned | — |
| POST | `/rest/fulfillment/picklist/trolley_tags` | Create trolley tag | planned | — |
| DELETE | `/rest/fulfillment/picklist/trolley_tags/{trolleyTag}` | Delete trolley tag | planned | — |
| GET | `/rest/fulfillment/picklist/trolley_tags/{trolleyTag}` | Get a pick list | planned | — |
| GET | `/rest/fulfillment/picklist/{id}` | Get a pick list | planned | — |
| POST | `/rest/fulfillment/picklist/{id}/{action}` | Execute a pick list action | planned | — |
| DELETE | `/rest/fulfillment/picklist/{pickingOrderId}/trolley_tags` | Delete trolley tag | planned | — |

### `Item`

4/294 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/availabilities` | List item availabilities | planned | — |
| GET | `/rest/availabilities/{id}` | Get an item availability | planned | — |
| PUT | `/rest/availabilities/{id}` | Update an item availability | planned | — |
| DELETE | `/rest/item_sets` | Delete item sets | planned | — |
| GET | `/rest/item_sets` | List item sets | planned | — |
| POST | `/rest/item_sets` | Create item sets | planned | — |
| PUT | `/rest/item_sets` | Update item sets | planned | — |
| DELETE | `/rest/item_sets/{id}` | Delete an item set | planned | — |
| GET | `/rest/item_sets/{id}` | Get an item set | planned | — |
| PUT | `/rest/item_sets/{id}` | Update an item set | planned | — |
| DELETE | `/rest/item_sets/{setId}/components` | Delete item set components | planned | — |
| GET | `/rest/item_sets/{setId}/components` | List item set components of an item set | planned | — |
| POST | `/rest/item_sets/{setId}/components` | Create item set components | planned | — |
| PUT | `/rest/item_sets/{setId}/components` | Update item set components | planned | — |
| DELETE | `/rest/item_sets/{setId}/components/{id}` | Delete an item set component | planned | — |
| GET | `/rest/item_sets/{setId}/components/{id}` | Get an item set component | planned | — |
| PUT | `/rest/item_sets/{setId}/components/{id}` | Update an item set component | planned | — |
| GET | `/rest/item_sets/{setId}/config` | Get the item set configuration of an item set | planned | — |
| PUT | `/rest/item_sets/{setId}/config` | Update an item set configuration | planned | — |
| POST | `/rest/item_sets/{setId}/config/sales_prices` | Trigger a sales price calculation for an item set | planned | — |
| GET | `/rest/items` | Search item | **implemented** | `items.list` |
| POST | `/rest/items` | Create new items | **implemented** | `items.create` |
| PUT | `/rest/items` | Bulk update items | planned | — |
| GET | `/rest/items/attribute_values/{valueId}/names` | Get name and language for an attribute value ID | planned | — |
| POST | `/rest/items/attribute_values/{valueId}/names` | Create an attribute value name | planned | — |
| DELETE | `/rest/items/attribute_values/{valueId}/names/{lang}` | Delete an attribute value name | planned | — |
| GET | `/rest/items/attribute_values/{valueId}/names/{lang}` | Get an attribute value name | planned | — |
| PUT | `/rest/items/attribute_values/{valueId}/names/{lang}` | Update an attribute value name | planned | — |
| GET | `/rest/items/attributes` | List attributes | planned | — |
| POST | `/rest/items/attributes` | Create an attribute | planned | — |
| GET | `/rest/items/attributes/maps` | Lists all attribute maps. | planned | — |
| POST | `/rest/items/attributes/markets/maps` | Creates a new attribute map. | planned | — |
| GET | `/rest/items/attributes/values/maps` | Lists all attribute value maps. | planned | — |
| POST | `/rest/items/attributes/values/markets/maps` | Creates a new attribute value map. | planned | — |
| DELETE | `/rest/items/attributes/{attributeId}/markets/{marketId}/maps` | Deletes an attribute map. | planned | — |
| GET | `/rest/items/attributes/{attributeId}/markets/{marketId}/maps` | Gets an attribute map. | planned | — |
| PUT | `/rest/items/attributes/{attributeId}/markets/{marketId}/maps` | Updates an attribute map. | planned | — |
| GET | `/rest/items/attributes/{attributeId}/names` | Get an attribute name | planned | — |
| POST | `/rest/items/attributes/{attributeId}/names` | Create an attribute name | planned | — |
| DELETE | `/rest/items/attributes/{attributeId}/names/{lang}` | Delete an attribute name | planned | — |
| GET | `/rest/items/attributes/{attributeId}/names/{lang}` | List attribute names | planned | — |
| PUT | `/rest/items/attributes/{attributeId}/names/{lang}` | Update an attribute name | planned | — |
| GET | `/rest/items/attributes/{attributeId}/value_market_names` | Search attribute value market names | planned | — |
| POST | `/rest/items/attributes/{attributeId}/value_market_names` | Create an attribute value market name | planned | — |
| DELETE | `/rest/items/attributes/{attributeId}/value_market_names/{valueId}/{lang}/{referenceType}` | Delete an attribute value market name | planned | — |
| PUT | `/rest/items/attributes/{attributeId}/value_market_names/{valueId}/{lang}/{referenceType}` | Update an attribute value market name | planned | — |
| GET | `/rest/items/attributes/{attributeId}/values` | List attribute values | planned | — |
| POST | `/rest/items/attributes/{attributeId}/values` | Create an attribute value | planned | — |
| DELETE | `/rest/items/attributes/{attributeId}/values/{attributeValueId}/markets/{marketId}/maps` | Deletes an attribute value map. | planned | — |
| GET | `/rest/items/attributes/{attributeId}/values/{attributeValueId}/markets/{marketId}/maps` | Gets an attribute value map. | planned | — |
| PUT | `/rest/items/attributes/{attributeId}/values/{attributeValueId}/markets/{marketId}/maps` | Updates an attribute value map. | planned | — |
| DELETE | `/rest/items/attributes/{attributeId}/values/{id}` | Delete an attribute value | planned | — |
| GET | `/rest/items/attributes/{attributeId}/values/{id}` | Get an attribute value | planned | — |
| PUT | `/rest/items/attributes/{attributeId}/values/{id}` | Update an attribute value | planned | — |
| DELETE | `/rest/items/attributes/{id}` | Delete an attribute | planned | — |
| GET | `/rest/items/attributes/{id}` | Get an attribute | planned | — |
| PUT | `/rest/items/attributes/{id}` | Update an attribute | planned | — |
| GET | `/rest/items/barcodes` | List barcodes | planned | — |
| POST | `/rest/items/barcodes` | Create a barcode | planned | — |
| GET | `/rest/items/barcodes/referrer/{referrerId}` | List barcodes by referrer | planned | — |
| GET | `/rest/items/barcodes/type/{type}` | List barcodes by type | planned | — |
| DELETE | `/rest/items/barcodes/{barcodeId}` | Delete a barcode | planned | — |
| GET | `/rest/items/barcodes/{barcodeId}` | Get a barcode | planned | — |
| PUT | `/rest/items/barcodes/{barcodeId}` | Update a barcode | planned | — |
| POST | `/rest/items/barcodes/{barcodeId}/referrer` | Activate a referrer | planned | — |
| DELETE | `/rest/items/barcodes/{barcodeId}/referrer/{referrerId}` | Deactivate a referrer | planned | — |
| GET | `/rest/items/item_shipping_profiles` | List all shipping profiles of all items | planned | — |
| POST | `/rest/items/item_shipping_profiles` | Bulk activate shipping profiles | planned | — |
| GET | `/rest/items/labels` | List item label templates | planned | — |
| GET | `/rest/items/listings/categories` | Search for item listing categories | planned | — |
| GET | `/rest/items/listings/categories/{id}` | Get one item listing categories | planned | — |
| GET | `/rest/items/listings/shop_categories/{ebayAccountId}` | Get a list of item listing shop categories | planned | — |
| GET | `/rest/items/manufacturers` | List manufacturers | planned | — |
| POST | `/rest/items/manufacturers` | Create a manufacturer | planned | — |
| DELETE | `/rest/items/manufacturers/{id}` | Delete a manufacturer | planned | — |
| GET | `/rest/items/manufacturers/{id}` | Get a manufacturer | planned | — |
| PUT | `/rest/items/manufacturers/{id}` | Update a manufacturer | planned | — |
| GET | `/rest/items/manufacturers/{id}/commissions` | List commissions | planned | — |
| POST | `/rest/items/manufacturers/{id}/commissions` | Create a commission | planned | — |
| DELETE | `/rest/items/manufacturers/{id}/commissions/{manufacturerId}` | Delete a commission | planned | — |
| GET | `/rest/items/manufacturers/{id}/commissions/{manufacturerId}` | Get a commission | planned | — |
| PUT | `/rest/items/manufacturers/{id}/commissions/{manufacturerId}` | Update a commission | planned | — |
| GET | `/rest/items/packing_units` | Get the item variation packing units | planned | — |
| GET | `/rest/items/packing_units/{id}` | Get the item variation packing unit for a specific given id | planned | — |
| GET | `/rest/items/properties` | List properties | planned | — |
| POST | `/rest/items/properties` | Create a property | planned | — |
| DELETE | `/rest/items/properties/{id}` | Delete a property | planned | — |
| GET | `/rest/items/properties/{id}` | Get a property | planned | — |
| PUT | `/rest/items/properties/{id}` | Update a property | planned | — |
| GET | `/rest/items/properties/{id}/market_references` | List property market references | planned | — |
| POST | `/rest/items/properties/{id}/market_references` | Create a property market reference | planned | — |
| DELETE | `/rest/items/properties/{id}/market_references/{marketId}` | Delete a property market reference | planned | — |
| GET | `/rest/items/properties/{id}/market_references/{marketId}` | Get a property market reference | planned | — |
| PUT | `/rest/items/properties/{id}/market_references/{marketId}` | Update a property market reference | planned | — |
| GET | `/rest/items/properties/{id}/names` | List the property names | planned | — |
| POST | `/rest/items/properties/{id}/names` | Create a property name | planned | — |
| DELETE | `/rest/items/properties/{id}/names/{lang}` | Delete a property name | planned | — |
| GET | `/rest/items/properties/{id}/names/{lang}` | Get a property name | planned | — |
| PUT | `/rest/items/properties/{id}/names/{lang}` | Update a property name | planned | — |
| GET | `/rest/items/properties/{propertyId}/selections` | List property selections | planned | — |
| POST | `/rest/items/properties/{propertyId}/selections` | Create a property selection | planned | — |
| DELETE | `/rest/items/properties/{propertyId}/selections/{id}` | Delete a property selection | planned | — |
| GET | `/rest/items/properties/{propertyId}/selections/{id}` | Get a property selection | planned | — |
| POST | `/rest/items/properties/{propertyId}/selections/{id}` | Creates a property selection lang | planned | — |
| DELETE | `/rest/items/properties/{propertyId}/selections/{id}/{lang}` | Delete a property selection language | planned | — |
| GET | `/rest/items/properties/{propertyId}/selections/{id}/{lang}` | List property selections by language | planned | — |
| PUT | `/rest/items/properties/{propertyId}/selections/{id}/{lang}` | Update a property selection | planned | — |
| GET | `/rest/items/properties/{propertyId}/selections/{lang}` | List property selections | planned | — |
| GET | `/rest/items/property_groups` | List property groups | planned | — |
| POST | `/rest/items/property_groups` | Create a property group | planned | — |
| DELETE | `/rest/items/property_groups/{id}` | Delete a property group | planned | — |
| GET | `/rest/items/property_groups/{id}` | Get a property group | planned | — |
| PUT | `/rest/items/property_groups/{id}` | Update a property group | planned | — |
| GET | `/rest/items/property_groups/{id}/names` | List the property group names of a property group | planned | — |
| POST | `/rest/items/property_groups/{id}/names` | Create a property group name | planned | — |
| DELETE | `/rest/items/property_groups/{id}/names/{lang}` | Delete a property group name | planned | — |
| GET | `/rest/items/property_groups/{id}/names/{lang}` | Get a property group name in a language | planned | — |
| PUT | `/rest/items/property_groups/{id}/names/{lang}` | Update a property group name | planned | — |
| GET | `/rest/items/sales_prices` | List sales prices | planned | — |
| POST | `/rest/items/sales_prices` | Create a sales price | planned | — |
| DELETE | `/rest/items/sales_prices/{id}` | Delete a sales price | planned | — |
| GET | `/rest/items/sales_prices/{id}` | Get a sales price | planned | — |
| PUT | `/rest/items/sales_prices/{id}` | Update a sales price | planned | — |
| GET | `/rest/items/sales_prices/{id}/accounts` | List referrer accounts | planned | — |
| POST | `/rest/items/sales_prices/{id}/accounts` | Activate a referrer account | planned | — |
| DELETE | `/rest/items/sales_prices/{id}/accounts/{accountType}/{accountId}` | Deactivate a referrer account | planned | — |
| GET | `/rest/items/sales_prices/{id}/countries` | List countries by sales price | planned | — |
| POST | `/rest/items/sales_prices/{id}/countries` | Activate a country | planned | — |
| DELETE | `/rest/items/sales_prices/{id}/countries/{countryId}` | Deactivate a country | planned | — |
| GET | `/rest/items/sales_prices/{id}/currencies` | List activated currencies | planned | — |
| POST | `/rest/items/sales_prices/{id}/currencies` | Activate a currency | planned | — |
| DELETE | `/rest/items/sales_prices/{id}/currencies/{currency}` | Deactivate a currency | planned | — |
| GET | `/rest/items/sales_prices/{id}/customer_classes` | List activated customer classes | planned | — |
| POST | `/rest/items/sales_prices/{id}/customer_classes` | Activate a customer class | planned | — |
| DELETE | `/rest/items/sales_prices/{id}/customer_classes/{customerClassId}` | Activate a customer class | planned | — |
| GET | `/rest/items/sales_prices/{id}/names` | List names of a sales price | planned | — |
| POST | `/rest/items/sales_prices/{id}/names` | Create a sales price name | planned | — |
| DELETE | `/rest/items/sales_prices/{id}/names/{lang}` | Delete a sales price name | planned | — |
| GET | `/rest/items/sales_prices/{id}/names/{lang}` | Gets a sales price name | planned | — |
| PUT | `/rest/items/sales_prices/{id}/names/{lang}` | Update a sales price name | planned | — |
| GET | `/rest/items/sales_prices/{id}/online_stores` | List activated clients (stores) | planned | — |
| POST | `/rest/items/sales_prices/{id}/online_stores` | Activate a client (store) | planned | — |
| DELETE | `/rest/items/sales_prices/{id}/online_stores/{webstoreId}` | Deactivate a client (store) | planned | — |
| GET | `/rest/items/sales_prices/{id}/referrers` | List activated referrers | planned | — |
| POST | `/rest/items/sales_prices/{id}/referrers` | Activate a referrer | planned | — |
| DELETE | `/rest/items/sales_prices/{id}/referrers/{referrerId}` | Deactivates a referrer | planned | — |
| GET | `/rest/items/units` | List units | planned | — |
| POST | `/rest/items/units` | Create a unit | planned | — |
| GET | `/rest/items/units/unitsOfMeasurements` | Get list with units of measurements | planned | — |
| DELETE | `/rest/items/units/{id}` | Delete a unit | planned | — |
| GET | `/rest/items/units/{id}` | Get a unit | planned | — |
| PUT | `/rest/items/units/{id}` | Update a unit | planned | — |
| GET | `/rest/items/units/{id}/names` | List unit names | planned | — |
| POST | `/rest/items/units/{id}/names` | Create a unit name | planned | — |
| DELETE | `/rest/items/units/{id}/names/{lang}` | Delete a unit name | planned | — |
| GET | `/rest/items/units/{id}/names/{lang}` | Get a unit name | planned | — |
| PUT | `/rest/items/units/{id}/names/{lang}` | Update a unit name | planned | — |
| GET | `/rest/items/variations` | Search variations | planned | — |
| PUT | `/rest/items/variations` | Update up to 50 variations | planned | — |
| POST | `/rest/items/variations/variation_categories` | Bulk create category links | planned | — |
| PUT | `/rest/items/variations/variation_categories` | Bulk update category links | planned | — |
| GET | `/rest/items/variations/variation_markets` | List all links between variations and markets | planned | — |
| POST | `/rest/items/variations/variation_markets` | Create up to 50 links between variations and markets | planned | — |
| POST | `/rest/items/variations/variation_properties` | Bulk update properties | planned | — |
| PUT | `/rest/items/variations/variation_properties` | Bulk update properties | planned | — |
| GET | `/rest/items/variations/variation_sales_prices` | Get all sales price relations | planned | — |
| POST | `/rest/items/variations/variation_sales_prices` | Bulk create prices | planned | — |
| PUT | `/rest/items/variations/variation_sales_prices` | Bulk update prices | planned | — |
| GET | `/rest/items/{id}/images` | List images of an item | planned | — |
| GET | `/rest/items/{id}/images/attribute_value_markets` | List attribute value image link | planned | — |
| POST | `/rest/items/{id}/images/upload` | Upload a new image | planned | — |
| DELETE | `/rest/items/{id}/images/{imageId}` | Delete an image | planned | — |
| GET | `/rest/items/{id}/images/{imageId}` | Get an image | planned | — |
| PUT | `/rest/items/{id}/images/{imageId}` | Update an image | planned | — |
| POST | `/rest/items/{id}/images/{imageId}/attribute_value_markets` | Create an attribute value image link | planned | — |
| DELETE | `/rest/items/{id}/images/{imageId}/attribute_value_markets/{valueId}` | Delete an attribute value image link | planned | — |
| GET | `/rest/items/{id}/images/{imageId}/attribute_value_markets/{valueId}` | Get an attribute value image link | planned | — |
| PUT | `/rest/items/{id}/images/{imageId}/attribute_value_markets/{valueId}` | Update an attribute value image link | planned | — |
| DELETE | `/rest/items/{id}/images/{imageId}/availabilities` | Delete an availability | planned | — |
| GET | `/rest/items/{id}/images/{imageId}/availabilities` | List availabilities | planned | — |
| POST | `/rest/items/{id}/images/{imageId}/availabilities` | Create an availability | planned | — |
| GET | `/rest/items/{id}/images/{imageId}/names` | List names of an image | planned | — |
| POST | `/rest/items/{id}/images/{imageId}/names` | Create an image name | planned | — |
| DELETE | `/rest/items/{id}/images/{imageId}/names/{lang}` | Delete an image name | planned | — |
| GET | `/rest/items/{id}/images/{imageId}/names/{lang}` | Get an image name | planned | — |
| PUT | `/rest/items/{id}/images/{imageId}/names/{lang}` | Update an image name | planned | — |
| GET | `/rest/items/{id}/images/{imageId}/variation_images` | List image links of an image | planned | — |
| GET | `/rest/items/{id}/item_cross_selling` | List cross-selling links | planned | — |
| POST | `/rest/items/{id}/item_cross_selling` | Create a cross-selling link | planned | — |
| DELETE | `/rest/items/{id}/item_cross_selling/{crossItemId}` | Delete a cross-selling link | planned | — |
| PUT | `/rest/items/{id}/item_cross_selling/{crossItemId}` | Update a cross-selling link | planned | — |
| POST | `/rest/items/{id}/labels` | Get a item label | planned | — |
| GET | `/rest/items/{id}/variation_images` | List image links of an item | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/descriptions` | List texts | planned | — |
| POST | `/rest/items/{id}/variations/{variationId}/descriptions` | Create texts | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/descriptions/{lang}` | Delete texts | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/descriptions/{lang}` | Get texts | planned | — |
| PUT | `/rest/items/{id}/variations/{variationId}/descriptions/{lang}` | Update texts | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/images` | List images of a variation | planned | — |
| POST | `/rest/items/{id}/variations/{variationId}/labels` | Get a variation label | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/market_ident_numbers` | List ident number of a variation | planned | — |
| POST | `/rest/items/{id}/variations/{variationId}/market_ident_numbers` | Create a market ident number | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/market_ident_numbers/{marketIdentNumberId}` | Deletes a market ident number | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/market_ident_numbers/{marketIdentNumberId}` | Get a market ident number | planned | — |
| PUT | `/rest/items/{id}/variations/{variationId}/market_ident_numbers/{marketIdentNumberId}` | Updates a market ident number | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/stock` | List stock of a variation per warehouse | planned | — |
| PUT | `/rest/items/{id}/variations/{variationId}/stock/bookIncomingItems` | Book incoming stock | planned | — |
| PUT | `/rest/items/{id}/variations/{variationId}/stock/bookOutgoingItems` | Book outgoing stock | planned | — |
| PUT | `/rest/items/{id}/variations/{variationId}/stock/correction` | Correct stock | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/stock/movements` | List stock movements | planned | — |
| PUT | `/rest/items/{id}/variations/{variationId}/stock/redistribute` | Redistribute stock | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/stock/storageLocations` | List stock of a variation per storage locations | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_additional_skus` | List additional SKUs | planned | — |
| POST | `/rest/items/{id}/variations/{variationId}/variation_additional_skus` | Create an additional SKU | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/variation_additional_skus/{additionalSkuId}` | Delete an additional SKU | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_additional_skus/{additionalSkuId}` | Gets an additional SKU | planned | — |
| PUT | `/rest/items/{id}/variations/{variationId}/variation_additional_skus/{additionalSkuId}` | Update an additional SKU | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_barcodes` | List variation barcodes | planned | — |
| POST | `/rest/items/{id}/variations/{variationId}/variation_barcodes` | Create a variation barcode | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/variation_barcodes/{barcodeId}` | Delete a variation barcode | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_barcodes/{barcodeId}` | Get a variation barcode | planned | — |
| PUT | `/rest/items/{id}/variations/{variationId}/variation_barcodes/{barcodeId}` | Update a variation barcode | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_bundles` | List bundle components | planned | — |
| POST | `/rest/items/{id}/variations/{variationId}/variation_bundles` | Add a variation to a bundle | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/variation_bundles/{bundleId}` | Remove a bundle component | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_bundles/{bundleId}` | Get a variation bundle | planned | — |
| PUT | `/rest/items/{id}/variations/{variationId}/variation_bundles/{bundleId}` | Update a variation bundle | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_categories` | List categories linked to a variation | planned | — |
| POST | `/rest/items/{id}/variations/{variationId}/variation_categories` | Link a category to a variation | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/variation_categories/{catId}` | Remove a category from a variation | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_categories/{catId}` | Get link between category and variation | planned | — |
| PUT | `/rest/items/{id}/variations/{variationId}/variation_categories/{catId}` | Update variation category link | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_clients` | List clients linked to a variation | planned | — |
| POST | `/rest/items/{id}/variations/{variationId}/variation_clients` | Link a client to a variation | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/variation_clients/{plentyId}` | Unlink a client from a variation | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_component_bundles` | List bundles | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_default_categories` | List default category links | planned | — |
| POST | `/rest/items/{id}/variations/{variationId}/variation_default_categories` | Create a default category link | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/variation_default_categories/{plentyId}` | Delete a default category link | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_default_categories/{plentyId}` | Gets a default category link | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_images` | List image links of a variation | planned | — |
| POST | `/rest/items/{id}/variations/{variationId}/variation_images` | Create an image link | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/variation_images/{imageId}` | Delete an image link | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/variation_markets` | Delete all market links of one variation | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_markets` | List markets linked to a variation | planned | — |
| POST | `/rest/items/{id}/variations/{variationId}/variation_markets` | Create link between variation and market | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/variation_markets/{marketplaceId}` | Delete link between variation and market | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/variation_properties` | Deletes all links between a variation and its property values | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_properties` | List property values linked to a variation | planned | — |
| POST | `/rest/items/{id}/variations/{variationId}/variation_properties` | Create link between variation and property value | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/variation_properties/{propertyId}` | Delete link between variation and property value | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_properties/{propertyId}` | Get a property value | planned | — |
| PUT | `/rest/items/{id}/variations/{variationId}/variation_properties/{propertyId}` | Update a property value | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/variation_sales_prices` | Delete all links between a variation and its sales prices | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_sales_prices` | List sales prices of a variation | planned | — |
| POST | `/rest/items/{id}/variations/{variationId}/variation_sales_prices` | Create link between variation and sales price | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/variation_sales_prices/{priceId}` | Delete link between variation and sales price | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_sales_prices/{priceId}` | Get sales price data for a variation | planned | — |
| PUT | `/rest/items/{id}/variations/{variationId}/variation_sales_prices/{priceId}` | Update sales price data | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_skus` | List SKUs | planned | — |
| POST | `/rest/items/{id}/variations/{variationId}/variation_skus` | Create an SKU | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/variation_skus/{skuId}` | Delete an SKU | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_skus/{skuId}` | Get an SKU | planned | — |
| PUT | `/rest/items/{id}/variations/{variationId}/variation_skus/{skuId}` | Update an SKU | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_suppliers` | Lists suppliers for a variation | planned | — |
| POST | `/rest/items/{id}/variations/{variationId}/variation_suppliers` | Create a link between variation and supplier | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/variation_suppliers/{variationSupplierId}` | Delete link between variation and supplier | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_suppliers/{variationSupplierId}` | Get supplier data for a variation | planned | — |
| PUT | `/rest/items/{id}/variations/{variationId}/variation_suppliers/{variationSupplierId}` | Updates supplier data for a variation | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_warehouses` | List the warehouses linked to a variation | planned | — |
| POST | `/rest/items/{id}/variations/{variationId}/variation_warehouses` | Create link between a variation and a warehouse | planned | — |
| DELETE | `/rest/items/{id}/variations/{variationId}/variation_warehouses/{warehouseId}` | Delete link between a warehouse and a variation | planned | — |
| GET | `/rest/items/{id}/variations/{variationId}/variation_warehouses/{warehouseId}` | Get warehouse data for a variation | planned | — |
| PUT | `/rest/items/{id}/variations/{variationId}/variation_warehouses/{warehouseId}` | Update warehouse data of a variation | planned | — |
| DELETE | `/rest/items/{itemId}` | Delete an item | planned | — |
| GET | `/rest/items/{itemId}` | Show an item | **implemented** | `items.get` |
| PUT | `/rest/items/{itemId}` | Update a item | **implemented** | `items.update` |
| POST | `/rest/items/{itemId}/copy` | Copies an item | planned | — |
| POST | `/rest/items/{itemId}/fill` | Fill item to es | planned | — |
| DELETE | `/rest/items/{itemId}/item_shipping_profiles` | Deactivate shipping profiles of an item | planned | — |
| GET | `/rest/items/{itemId}/item_shipping_profiles` | List shipping profiles of an item | planned | — |
| POST | `/rest/items/{itemId}/item_shipping_profiles` | Activate a shipping profile | planned | — |
| DELETE | `/rest/items/{itemId}/item_shipping_profiles/{id}` | Deactivate a shipping profile | planned | — |
| GET | `/rest/items/{itemId}/variations` | List variations of an item | planned | — |
| POST | `/rest/items/{itemId}/variations` | Create a variation | planned | — |
| DELETE | `/rest/items/{itemId}/variations/{variationId}` | Delete a variation | planned | — |
| GET | `/rest/items/{itemId}/variations/{variationId}` | Get a variation | planned | — |
| PUT | `/rest/items/{itemId}/variations/{variationId}` | Update a variation | planned | — |
| POST | `/rest/items/{itemId}/variations/{variationId}/fill` | Fill a variation | planned | — |
| GET | `/rest/items/{itemId}/variations/{variationId}/variation_properties/{propertyId}/texts` | Get property value texts | planned | — |
| POST | `/rest/items/{itemId}/variations/{variationId}/variation_properties/{propertyId}/texts` | Create property value text by language | planned | — |
| DELETE | `/rest/items/{itemId}/variations/{variationId}/variation_properties/{propertyId}/texts/{lang}` | Delete property value text by language | planned | — |
| GET | `/rest/items/{itemId}/variations/{variationId}/variation_properties/{propertyId}/texts/{lang}` | Get property value text by language | planned | — |
| PUT | `/rest/items/{itemId}/variations/{variationId}/variation_properties/{propertyId}/texts/{lang}` | Update property value text by language | planned | — |

### `LegalInformation`

0/4 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/legalinformation/all/{plentyId}/{lang}` | Return ALL legal texts | planned | — |
| POST | `/rest/legalinformation/all/{plentyId}/{lang}` | update the text in the plenty_text table | planned | — |
| GET | `/rest/legalinformation/{plentyId}/{lang}/{type}` | Get legal information of an online store | planned | — |
| PUT | `/rest/legalinformation/{plentyId}/{lang}/{type}` | Save legal information for an online store | planned | — |

### `Listing`

0/48 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/listings` | List listing | planned | — |
| POST | `/rest/listings` | Create new listing | planned | — |
| POST | `/rest/listings/layout_templates` | Create new layout template | planned | — |
| DELETE | `/rest/listings/layout_templates/{id}` | Delete a layout template | planned | — |
| GET | `/rest/listings/layout_templates/{id}` | Get a layout template | planned | — |
| GET | `/rest/listings/markets` | List listing markets | planned | — |
| POST | `/rest/listings/markets` | Create new listing market | planned | — |
| GET | `/rest/listings/markets/directories` | Get all listing market directories | planned | — |
| POST | `/rest/listings/markets/directories` | Create listing market directory | planned | — |
| DELETE | `/rest/listings/markets/directories/{id}` | Delete listing market directory | planned | — |
| GET | `/rest/listings/markets/directories/{id}` | Get a listing market directory | planned | — |
| PUT | `/rest/listings/markets/directories/{id}` | Update listing market directory | planned | — |
| GET | `/rest/listings/markets/find` | Find listing markets | planned | — |
| GET | `/rest/listings/markets/histories` | List listing market history | planned | — |
| DELETE | `/rest/listings/markets/histories/end/{id?}` | End the listing | planned | — |
| POST | `/rest/listings/markets/histories/relist/{id?}` | Relist the listing | planned | — |
| PUT | `/rest/listings/markets/histories/update/{id?}` | Update listing market histories | planned | — |
| GET | `/rest/listings/markets/histories/{id}` | Get a listing market history | planned | — |
| GET | `/rest/listings/markets/infos` | Search listing market info | planned | — |
| GET | `/rest/listings/markets/item_specifics` | Gets all ListingMarketItemSpecifics. | planned | — |
| GET | `/rest/listings/markets/item_specifics/find` | Gets all ListingMarketItemSpecifics. | planned | — |
| DELETE | `/rest/listings/markets/item_specifics/{id}` | Deletes a ListingMarketItemSpecific. | planned | — |
| GET | `/rest/listings/markets/item_specifics/{id}` | Gets a ListingMarketItemSpecific. | planned | — |
| PUT | `/rest/listings/markets/item_specifics/{id}` | Updates a ListingMarketItemSpecific. | planned | — |
| POST | `/rest/listings/markets/start/{id?}` | Start the market listing on the designated market. | planned | — |
| GET | `/rest/listings/markets/texts` | List listing market texts | planned | — |
| POST | `/rest/listings/markets/texts` | Create a listing market text | planned | — |
| DELETE | `/rest/listings/markets/texts/{id}` | Delete a listing market text | planned | — |
| GET | `/rest/listings/markets/texts/{id}` | Get a listing market text | planned | — |
| PUT | `/rest/listings/markets/texts/{listingMarketId}/{lang}` | Update a listing market text | planned | — |
| POST | `/rest/listings/markets/verify/{id?}` | Verify listing markets | planned | — |
| DELETE | `/rest/listings/markets/{id}` | Delete listing market | planned | — |
| GET | `/rest/listings/markets/{id}` | Get a listing market | planned | — |
| PUT | `/rest/listings/markets/{id}` | Update a listing market | planned | — |
| POST | `/rest/listings/option_templates` | Create option template | planned | — |
| GET | `/rest/listings/option_templates/preview` | Get a preview list of option templates | planned | — |
| DELETE | `/rest/listings/option_templates/{id}` | Delete option template | planned | — |
| GET | `/rest/listings/option_templates/{id}` | Get option template | planned | — |
| PUT | `/rest/listings/option_templates/{id}` | Update option template | planned | — |
| GET | `/rest/listings/shipping_profiles` | List listing shipping profiles | planned | — |
| GET | `/rest/listings/shipping_profiles/{id}` | Get a shipping profile | planned | — |
| GET | `/rest/listings/stock_dependence_types` | List listing stock dependence types | planned | — |
| GET | `/rest/listings/stock_dependence_types/{id}` | Get a listing stock dependence type | planned | — |
| GET | `/rest/listings/types` | List listing types | planned | — |
| GET | `/rest/listings/types/{id}` | Get a listing type | planned | — |
| DELETE | `/rest/listings/{id}` | Delete a listing | planned | — |
| GET | `/rest/listings/{id}` | Get a listing | planned | — |
| PUT | `/rest/listings/{id}` | Update a listing | planned | — |

### `Log`

0/8 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/delete_log` | Search the delete log | planned | — |
| GET | `/rest/logs` | Search operation | planned | — |
| POST | `/rest/logs` | Create a log entry. | planned | — |
| GET | `/rest/logs/integration_keys` | Get integration keys | planned | — |
| GET | `/rest/logs/reference_types` | Get reference types | planned | — |
| GET | `/rest/logs/settings` | Show config. | planned | — |
| POST | `/rest/logs/settings` | Save config | planned | — |
| GET | `/rest/logs/{id}` | Get Log entry by ID. | planned | — |

### `MailTemplates`

0/9 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/mail_templates/email_service/accounts` | List all email accounts that can be used to send emails (e.g. Webstore or Messenger inboxes) | planned | — |
| POST | `/rest/mail_templates/email_service/addToFavourites/{templateId}` | Add template to favourites for current user | planned | — |
| GET | `/rest/mail_templates/email_service/getRecipient` | Get the email of a contact or order based on the receiver type | planned | — |
| GET | `/rest/mail_templates/email_service/history` | List all sent email for a specific entity (e.g order, contact, etc.) | planned | — |
| GET | `/rest/mail_templates/email_service/loadPreview/{templateId}` | Generates a render preview of a specific template (including attachments) | planned | — |
| POST | `/rest/mail_templates/email_service/removeFromFavourites/{templateId}` | Remove template from favourites for current user | planned | — |
| POST | `/rest/mail_templates/email_service/sendEmail/{templateId}` | Renders a template and sends an email to the specified recipients | planned | — |
| POST | `/rest/mail_templates/email_service/sendPreview` | Sends a direct email to the specified recipients (a preview of a template or any other custom content email) | planned | — |
| GET | `/rest/mail_templates/email_service/templatesTree` | List all EmailBuilder templates and folders structured as a nested tree | planned | — |

### `Market`

0/43 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/markets/credentials` | List credentials | planned | — |
| POST | `/rest/markets/credentials` | Create a credential | planned | — |
| GET | `/rest/markets/credentials/all` | List all credentials | planned | — |
| DELETE | `/rest/markets/credentials/{credentialsId}` | Delete a credential | planned | — |
| GET | `/rest/markets/credentials/{credentialsId}` | Get a credential | planned | — |
| PUT | `/rest/markets/credentials/{credentialsId}` | Update a credential | planned | — |
| GET | `/rest/markets/ebay/auth/login` | Get the login URL. | planned | — |
| PUT | `/rest/markets/ebay/auth/refresh-token` | Refresh an expired access token. | planned | — |
| GET | `/rest/markets/ebay/categories` | List categories | planned | — |
| GET | `/rest/markets/ebay/categories/{id}` | Get category | planned | — |
| POST | `/rest/markets/ebay/fulfillment_policies` | Create fulfillment policy | planned | — |
| DELETE | `/rest/markets/ebay/fulfillment_policies/{id}` | Delete fulfillment policy | planned | — |
| GET | `/rest/markets/ebay/fulfillment_policies/{id}` | Get fulfillment policy | planned | — |
| POST | `/rest/markets/ebay/fulfillment_policies/{id}` | Update fulfillment policy | planned | — |
| GET | `/rest/markets/ebay/item_specifics` | List item specifics | planned | — |
| GET | `/rest/markets/ebay/marketplaces` | Get all eBay marketplaces. | planned | — |
| GET | `/rest/markets/ebay/parts-fitments` | List fitments | planned | — |
| POST | `/rest/markets/ebay/parts-fitments` | Create a fitment | planned | — |
| GET | `/rest/markets/ebay/parts-fitments/search` | Search fitments | planned | — |
| DELETE | `/rest/markets/ebay/parts-fitments/{fitmentId}` | Delete a fitment. | planned | — |
| GET | `/rest/markets/ebay/parts-fitments/{fitmentId}` | Get a fitment | planned | — |
| PUT | `/rest/markets/ebay/parts-fitments/{fitmentId}` | Update fitment. | planned | — |
| POST | `/rest/markets/ebay/payment_policies` | Create payment policy | planned | — |
| DELETE | `/rest/markets/ebay/payment_policies/{id}` | Delete payment policy | planned | — |
| GET | `/rest/markets/ebay/payment_policies/{id}` | Get payment policy | planned | — |
| POST | `/rest/markets/ebay/payment_policies/{id}` | Update payment policy | planned | — |
| POST | `/rest/markets/ebay/return_policies` | Create return policy | planned | — |
| DELETE | `/rest/markets/ebay/return_policies/{id}` | Delete payment policy | planned | — |
| GET | `/rest/markets/ebay/return_policies/{id}` | Get return policy | planned | — |
| POST | `/rest/markets/ebay/return_policies/{id}` | Update return policy | planned | — |
| GET | `/rest/markets/ebay/shop_categories` | List all eBay shop categories | planned | — |
| GET | `/rest/markets/ebay/transactions` | List transactions | planned | — |
| GET | `/rest/markets/listings/marketplaces` | Get all listing marketplaces. | planned | — |
| GET | `/rest/markets/settings` | List market settings | planned | — |
| POST | `/rest/markets/settings` | Create market settings | planned | — |
| POST | `/rest/markets/settings/bulk` | Create market settings | planned | — |
| PUT | `/rest/markets/settings/bulk` | Update market settings | planned | — |
| GET | `/rest/markets/settings/correlations` | List correlation | planned | — |
| POST | `/rest/markets/settings/correlations` | Create a correlation | planned | — |
| POST | `/rest/markets/settings/correlations/bulk` | Create multiple correlations | planned | — |
| DELETE | `/rest/markets/settings/{settingId}` | Delete market settings | planned | — |
| GET | `/rest/markets/settings/{settingId}` | Get market settings | planned | — |
| PUT | `/rest/markets/settings/{settingId}` | Update market settings | planned | — |

### `Messenger`

0/92 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| DELETE | `/rest/conversations` | Deletes a batch of conversations | planned | — |
| GET | `/rest/conversations` | List conversation based on provided parameters | planned | — |
| POST | `/rest/conversations` | Create a new conversation | planned | — |
| PUT | `/rest/conversations/archive` | Move multiple conversations to archive | planned | — |
| DELETE | `/rest/conversations/archiveDelete` | Permanently delete a list of archived conversation | planned | — |
| PUT | `/rest/conversations/archiveRestore` | Restore multiple conversations from archive | planned | — |
| PUT | `/rest/conversations/batchRestoreConversations` | Restore deleted conversations from trash | planned | — |
| PUT | `/rest/conversations/batch_update_conversations` | Update batch of conversations | planned | — |
| DELETE | `/rest/conversations/categories` | Deletes a batch of categories | planned | — |
| GET | `/rest/conversations/categories` | Returns a paginated result object will list of conversation categories | planned | — |
| POST | `/rest/conversations/categories` | Creates a new category | planned | — |
| DELETE | `/rest/conversations/categories/{id}` | Deletes a single category (soft delete, type will be flagged as deleted) | planned | — |
| GET | `/rest/conversations/categories/{id}` | Retrieves a single category based on ID | planned | — |
| PUT | `/rest/conversations/categories/{id}` | Updates an existing category | planned | — |
| PUT | `/rest/conversations/categories/{id}/status` | Updates category status | planned | — |
| PUT | `/rest/conversations/close` | Updates the state for a batch of conversations | planned | — |
| PUT | `/rest/conversations/deadline` | Update deadline for a batch of conversations | planned | — |
| DELETE | `/rest/conversations/emptyTrash` | Adds the empty trash command to a queue | planned | — |
| GET | `/rest/conversations/events` | Returns a paginated result object will list of conversation events | planned | — |
| POST | `/rest/conversations/events` | Creates a new event | planned | — |
| DELETE | `/rest/conversations/events/{id}` | Deletes a single event | planned | — |
| PUT | `/rest/conversations/events/{id}` | Updates an existing event | planned | — |
| PUT | `/rest/conversations/events/{id}/copy` | Copies an event to a new event | planned | — |
| PUT | `/rest/conversations/events/{id}/updateExecutedAtEvent` | Sets the last execution date for an existing event | planned | — |
| PUT | `/rest/conversations/events/{id}/update_status` | Sets an event as active / inactive | planned | — |
| GET | `/rest/conversations/folders` | Returns a paginated result object will list of folders | planned | — |
| POST | `/rest/conversations/folders` | Creates a new folder | planned | — |
| PUT | `/rest/conversations/folders` | Assigns a batch of conversations to a batch of folders | planned | — |
| PUT | `/rest/conversations/folders/add` | Add multiple conversations to multiple folders | planned | — |
| PUT | `/rest/conversations/folders/remove` | Remove multiple conversations from multiple folders | planned | — |
| DELETE | `/rest/conversations/folders/{uuid5}` | Deletes a folder | planned | — |
| GET | `/rest/conversations/folders/{uuid5}` | Retrieves a folder object based on UUID | planned | — |
| PUT | `/rest/conversations/folders/{uuid5}` | Updates an existing folder | planned | — |
| PUT | `/rest/conversations/followUpDate` | Update follow up date for a batch of conversations | planned | — |
| GET | `/rest/conversations/history/{uuid5}` | Retrieves history for a conversation | planned | — |
| GET | `/rest/conversations/inboxes` | Returns a list with all configured inboxes | planned | — |
| PUT | `/rest/conversations/owner` | Update owner roles for specific conversation id/ids | planned | — |
| PUT | `/rest/conversations/priority` | Updates priority for a batch of conversations | planned | — |
| PUT | `/rest/conversations/read` | Mark a batch of conversations as read or unread | planned | — |
| DELETE | `/rest/conversations/removeRelation` | Remove conversation relation | planned | — |
| DELETE | `/rest/conversations/roles` | Delete a batch of roles | planned | — |
| GET | `/rest/conversations/roles` | Returns a paginated result object with list of roles | planned | — |
| POST | `/rest/conversations/roles` | Create new role | planned | — |
| DELETE | `/rest/conversations/roles/{id}` | Delete a role by ID | planned | — |
| GET | `/rest/conversations/roles/{id}` | Retrieves a role object based on role id | planned | — |
| PUT | `/rest/conversations/roles/{id}` | Updates an existing role | planned | — |
| POST | `/rest/conversations/search` | Search conversation based on provided parameters | planned | — |
| GET | `/rest/conversations/searchReceiver` | Searches for entities that can be linked to a conversation | planned | — |
| DELETE | `/rest/conversations/statuses` | Deletes a batch of statuses | planned | — |
| GET | `/rest/conversations/statuses` | Returns a paginated result object will list of conversation statuses | planned | — |
| POST | `/rest/conversations/statuses` | Creates a new status | planned | — |
| DELETE | `/rest/conversations/statuses/{id}` | Deletes a single status | planned | — |
| GET | `/rest/conversations/statuses/{id}` | Retrieves a single status based on ID | planned | — |
| PUT | `/rest/conversations/statuses/{id}` | Updates an existing status | planned | — |
| PUT | `/rest/conversations/subscribe` | Subscribes the current user to multiple conversations | planned | — |
| PUT | `/rest/conversations/tags` | Adds multiple tags to multiple conversations | planned | — |
| GET | `/rest/conversations/totals` | Returns the total number of unread conversations for current user | planned | — |
| PUT | `/rest/conversations/type_status` | Updates type and status for a batch of conversations | planned | — |
| DELETE | `/rest/conversations/types` | Deletes a batch of types | planned | — |
| GET | `/rest/conversations/types` | Returns a paginated result object will list of conversation types | planned | — |
| POST | `/rest/conversations/types` | Creates a new type | planned | — |
| DELETE | `/rest/conversations/types/{id}` | Deletes a single type | planned | — |
| GET | `/rest/conversations/types/{id}` | Retrieves a single type based on ID | planned | — |
| PUT | `/rest/conversations/types/{id}` | Updates an existing type | planned | — |
| PUT | `/rest/conversations/unsubscribe` | Unsubscribe the current user from multiple conversations | planned | — |
| DELETE | `/rest/conversations/{uuid5}` | Deletes a conversation | planned | — |
| GET | `/rest/conversations/{uuid5}` | Get a single conversation by UUID | planned | — |
| PUT | `/rest/conversations/{uuid5}` | Updates a conversation by UUID | planned | — |
| PUT | `/rest/conversations/{uuid5}/subscribe` | Subscribes a user to a conversation | planned | — |
| PUT | `/rest/conversations/{uuid5}/tags` | Adds tags to a single conversation | planned | — |
| PUT | `/rest/conversations/{uuid5}/unsubscribe` | Unsubscribes a user from a conversation | planned | — |
| GET | `/rest/messages` | List message stream of a certain message (excluding message with UUID5) | planned | — |
| POST | `/rest/messages` | Create message | planned | — |
| GET | `/rest/messages/forArchivedConversation` | List archived message stream of a certain conversation | planned | — |
| GET | `/rest/messages/get` | List messages per page | planned | — |
| DELETE | `/rest/messages/{uuid5}` | Delete message by UUID | planned | — |
| GET | `/rest/messages/{uuid5}` | Get message for the given UUID5 and all its associated successors | planned | — |
| GET | `/rest/messages/{uuid5}/attachments` | Get attachment by UUID and file name | planned | — |
| GET | `/rest/messages/{uuid5}/attachments/all` | Get all attachments by UUID | planned | — |
| PUT | `/rest/messages/{uuid5}/controls` | Update message controls | planned | — |
| PUT | `/rest/messages/{uuid5}/done` | Set or unset doneAt date of message | planned | — |
| PUT | `/rest/messages/{uuid5}/readBy` | Update ReadBy array of message | planned | — |
| PUT | `/rest/messages/{uuid5}/tags` | Update tags of message | planned | — |
| PUT | `/rest/messages/{uuid5}/visibility` | Update message visibility | planned | — |
| POST | `/rest/messenger/marketplaces/ebay` | Create new Ebay account | planned | — |
| PUT | `/rest/messenger/marketplaces/ebay` | Updates an existing Ebay account | planned | — |
| GET | `/rest/messenger/marketplaces/ebay/all` | Get the list of ebay accounts | planned | — |
| DELETE | `/rest/messenger/marketplaces/ebay/{id}` | Mark as deleted an Ebay account. | planned | — |
| GET | `/rest/messenger/marketplaces/ebay/{id}` | Retrieves an Ebay account object | planned | — |
| GET | `/rest/messenger/settings` | Retrieves the general settings object | planned | — |
| PUT | `/rest/messenger/settings` | Updates the general settings object | planned | — |
| GET | `/rest/messenger/settings/getDefaultWhisperMode` | Retrieves the default value for whisper mode | planned | — |

### `Newsletter`

0/21 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| DELETE | `/rest/newsletters` | Delete entries | planned | — |
| GET | `/rest/newsletters` | List newsletter entries | planned | — |
| POST | `/rest/newsletters` | Create entry | planned | — |
| POST | `/rest/newsletters/double_opt_in/{contactId}` | Send doubleOptIn mail | planned | — |
| DELETE | `/rest/newsletters/folders` | Delete folders | planned | — |
| GET | `/rest/newsletters/folders` | List newsletter folders | planned | — |
| POST | `/rest/newsletters/folders` | Create folder | planned | — |
| DELETE | `/rest/newsletters/folders/{folderId}` | Delete folder | planned | — |
| GET | `/rest/newsletters/folders/{folderId}` | List details of a folder | planned | — |
| PUT | `/rest/newsletters/folders/{folderId}` | Update folder | planned | — |
| GET | `/rest/newsletters/folders/{folderId}/recipients` | List all recipients of a folder | planned | — |
| GET | `/rest/newsletters/list_recipients` | List recipients | planned | — |
| DELETE | `/rest/newsletters/recipients` | Delete recipients | planned | — |
| GET | `/rest/newsletters/recipients` | List recipients of folder | planned | — |
| POST | `/rest/newsletters/recipients` | Create recipient | planned | — |
| DELETE | `/rest/newsletters/recipients/{recipientId}` | Delete recipient | planned | — |
| GET | `/rest/newsletters/recipients/{recipientId}` | List recipient | planned | — |
| PUT | `/rest/newsletters/recipients/{recipientId}` | Update recipient | planned | — |
| DELETE | `/rest/newsletters/{entryId}` | Delete entry | planned | — |
| GET | `/rest/newsletters/{entryId}` | List details of an entry | planned | — |
| PUT | `/rest/newsletters/{entryId}` | Update entry | planned | — |

### `Order`

69/307 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| POST | `/rest/advance_orders` | Create an advance order | planned | — |
| POST | `/rest/advance_orders/items/{orderItemId}/assign_variation` | Change an order item of type "unassigned variation" to "variation". | planned | — |
| POST | `/rest/advance_orders/items/{orderItemId}/unassign_variation` | Change an order item of type "variation" to "unassigned variation". | planned | — |
| POST | `/rest/advance_orders/preview` | Get an advance order create preview. | planned | — |
| DELETE | `/rest/advance_orders/{orderId}` | Delete an advance order | planned | — |
| PUT | `/rest/advance_orders/{orderId}` | Update an advance order | planned | — |
| PUT | `/rest/advance_orders/{orderId}/preview` | Get an advance order update preview | planned | — |
| POST | `/rest/credit_notes` | Create a credit note | planned | — |
| POST | `/rest/credit_notes/items/{orderItemId}/assign_variation` | Change an order item of type "unassigned variation" to "variation". | planned | — |
| POST | `/rest/credit_notes/items/{orderItemId}/unassign_variation` | Change an order item of type "variation" to "unassigned variation". | planned | — |
| POST | `/rest/credit_notes/preview` | Get a credit note create preview. | planned | — |
| DELETE | `/rest/credit_notes/{orderId}` | Delete a credit note | planned | — |
| PUT | `/rest/credit_notes/{orderId}` | Update a credit note | planned | — |
| PUT | `/rest/credit_notes/{orderId}/preview` | Get a credit note update preview | planned | — |
| POST | `/rest/delivery_orders` | Create a delivery order | planned | — |
| POST | `/rest/delivery_orders/items/{orderItemId}/assign_variation` | Change an order item of type "unassigned variation" to "variation". | planned | — |
| POST | `/rest/delivery_orders/items/{orderItemId}/unassign_variation` | Change an order item of type "variation" to "unassigned variation". | planned | — |
| POST | `/rest/delivery_orders/preview` | Get a delivery order create preview. | planned | — |
| DELETE | `/rest/delivery_orders/{orderId}` | Delete a delivery order | planned | — |
| PUT | `/rest/delivery_orders/{orderId}` | Update a delivery order | planned | — |
| POST | `/rest/delivery_orders/{orderId}/book` | Book out order items | planned | — |
| POST | `/rest/delivery_orders/{orderId}/cancel_booking` | Revert outgoing stock | planned | — |
| POST | `/rest/delivery_orders/{orderId}/cancel_booking/validate` | Validate cancellation of the booking of an order | planned | — |
| PUT | `/rest/delivery_orders/{orderId}/preview` | Get a delivery order update preview | planned | — |
| DELETE | `/rest/multi_credit_notes/{orderId}` | Delete a multi credit note | planned | — |
| PUT | `/rest/multi_credit_notes/{orderId}` | Update a multi credit note | planned | — |
| DELETE | `/rest/multi_orders/{orderId}` | Delete a multi sales order | planned | — |
| PUT | `/rest/multi_orders/{orderId}` | Update a multi order | planned | — |
| POST | `/rest/offers` | Create an offer | planned | — |
| POST | `/rest/offers/items/{orderItemId}/assign_variation` | Change an order item of type "unassigned variation" to "variation". | planned | — |
| POST | `/rest/offers/items/{orderItemId}/unassign_variation` | Change an order item of type "variation" to "unassigned variation". | planned | — |
| POST | `/rest/offers/preview` | Get an offer create preview. | planned | — |
| DELETE | `/rest/offers/{orderId}` | Delete an offer | planned | — |
| PUT | `/rest/offers/{orderId}` | Update an offer | planned | — |
| PUT | `/rest/offers/{orderId}/preview` | Get an offer update preview | planned | — |
| GET | `/rest/orders` | Search order | **implemented** | `orders.list` |
| POST | `/rest/orders` | Create an order | **implemented** | `orders.create` |
| GET | `/rest/orders/batch` | Get orders | **implemented** | `orders.get_orders_batch` |
| GET | `/rest/orders/contacts/{contactId}` | List orders of a contact | **implemented** | `orders.list_contact_orders` |
| POST | `/rest/orders/contacts/{contactId}/multi_order` | Create a multi-order | **implemented** | `orders.create_multi_order` |
| GET | `/rest/orders/coupons/campaigns` | Get list of campaigns | planned | — |
| DELETE | `/rest/orders/coupons/campaigns/codes/{code}` | Delete a coupon | planned | — |
| GET | `/rest/orders/coupons/campaigns/codes/{code}` | Get coupon code information | planned | — |
| PUT | `/rest/orders/coupons/campaigns/codes/{code}/disabled/{isDisabled}` | Disable or enable coupon | planned | — |
| GET | `/rest/orders/coupons/campaigns/{campaignId}` | Get campaign by Id | planned | — |
| POST | `/rest/orders/coupons/campaigns/{campaignId}/codes` | Create a coupon code | planned | — |
| POST | `/rest/orders/coupons/codes` | Validate multiple coupons | planned | — |
| GET | `/rest/orders/coupons/codes/contacts/{contactId}` | List redeemed coupon codes of a contact | planned | — |
| POST | `/rest/orders/coupons/codes/{coupon}` | Validate a coupon | planned | — |
| GET | `/rest/orders/currencies` | List currencies | planned | — |
| GET | `/rest/orders/currencies/countries/{countryId}` | Get a currency for a country | planned | — |
| GET | `/rest/orders/currencies/exchange_rates/from/{currencyIso}` | Get the exchange rates from a currency | planned | — |
| GET | `/rest/orders/currencies/exchange_rates/to/{currencyIso}` | Get the exchange rates to a currency | planned | — |
| GET | `/rest/orders/currencies/{currencyIso}` | Get a currency | planned | — |
| GET | `/rest/orders/currencies/{currencyIso}/countries` | List countries for a currency | planned | — |
| GET | `/rest/orders/currencies/{currencyIso}/exchangeRate` | Get the exchange rate for a currency | planned | — |
| GET | `/rest/orders/dates/types` | List order date types | **implemented** | `orders.list_date_types` |
| GET | `/rest/orders/dates/types/{typeId}` | Find an order date type | **implemented** | `orders.get_date_type` |
| GET | `/rest/orders/dates/types/{typeId}/names` | List names of an order date type | **implemented** | `orders.list_date_type_names` |
| GET | `/rest/orders/dates/types/{typeId}/names/{lang}` | Get a name of an order date type | **implemented** | `orders.get_date_type_name` |
| GET | `/rest/orders/documents/accounting_summary` | List document accounting summaries | **implemented** | `orders.list_accounting_summaries` |
| POST | `/rest/orders/items/dates` | Create a date for an order item | **implemented** (deprecated by PlentyMarkets) | `orders.create_item_date` |
| DELETE | `/rest/orders/items/dates/{id}` | Delete a date of an order item | **implemented** (deprecated by PlentyMarkets) | `orders.delete_item_date` |
| GET | `/rest/orders/items/dates/{id}` | Get date of an order item | **implemented** (deprecated by PlentyMarkets) | `orders.get_item_date` |
| PUT | `/rest/orders/items/dates/{id}` | Update a date of an order item | **implemented** (deprecated by PlentyMarkets) | `orders.update_item_date` |
| DELETE | `/rest/orders/items/outgoing_stocks` | Revert outgoing stock for order items | **implemented** | `orders.revert_item_outgoing_stock` |
| POST | `/rest/orders/items/properties` | Create order item property | **implemented** | `orders.create_item_property` |
| DELETE | `/rest/orders/items/properties/{id}` | Delete order item property | **implemented** | `orders.delete_item_property` |
| GET | `/rest/orders/items/properties/{id}` | Get order item property | **implemented** | `orders.get_item_property` |
| PUT | `/rest/orders/items/properties/{id}` | Update order item property | **implemented** | `orders.update_item_property` |
| GET | `/rest/orders/items/transactions` | Search order item transactions | **implemented** | `orders.search_item_transactions` |
| POST | `/rest/orders/items/transactions/booking` | Book order item transactions | **implemented** | `orders.book_item_transactions` |
| DELETE | `/rest/orders/items/transactions/{transactionId}` | Delete order item transaction | **implemented** | `orders.delete_item_transaction` |
| PUT | `/rest/orders/items/transactions/{transactionId}` | Update order item transaction | **implemented** | `orders.update_item_transaction` |
| POST | `/rest/orders/items/{orderItemId}/booking` | Book an order item in | **implemented** | `orders.book_item_in` |
| GET | `/rest/orders/items/{orderItemId}/dates` | List all dates of an order item | **implemented** | `orders.list_item_dates` |
| DELETE | `/rest/orders/items/{orderItemId}/dates/{typeId}` | Delete a date of an order item by order item and date type | **implemented** | `orders.delete_item_date_by_type` |
| GET | `/rest/orders/items/{orderItemId}/dates/{typeId}` | Get a date of an order item by order item and date type | **implemented** | `orders.get_item_date_by_type` |
| POST | `/rest/orders/items/{orderItemId}/dates/{typeId}` | Create a date for an order item by order item and date type | **implemented** | `orders.create_item_date_by_type` |
| PUT | `/rest/orders/items/{orderItemId}/dates/{typeId}` | Update a date of an order item by order item and date type | **implemented** | `orders.update_item_date_by_type` |
| GET | `/rest/orders/items/{orderItemId}/properties` | Get all order item properties | deprecated (use `PUT /rest/orders/{orderId}`) | — |
| DELETE | `/rest/orders/items/{orderItemId}/properties/{typeId}` | Delete order item property | deprecated (use `PUT /rest/orders/{orderId}`) | — |
| GET | `/rest/orders/items/{orderItemId}/properties/{typeId}` | Get order item property | deprecated (use `PUT /rest/orders/{orderId}`) | — |
| POST | `/rest/orders/items/{orderItemId}/properties/{typeId}` | Create order item property | deprecated (use `PUT /rest/orders/{orderId}`) | — |
| PUT | `/rest/orders/items/{orderItemId}/properties/{typeId}` | Update order item property | deprecated (use `PUT /rest/orders/{orderId}`) | — |
| GET | `/rest/orders/items/{orderItemId}/transactions` | List order item transactions | **implemented** | `orders.list_item_transactions` |
| POST | `/rest/orders/items/{orderItemId}/transactions` | Create order item transaction | **implemented** | `orders.create_item_transaction` |
| GET | `/rest/orders/properties/types` | List order property types | **implemented** | `orders.list_property_types` |
| POST | `/rest/orders/properties/types` | Create order property type | **implemented** | `orders.create_property_type` |
| DELETE | `/rest/orders/properties/types/{typeId}` | Delete property type | **implemented** | `orders.delete_property_type` |
| GET | `/rest/orders/properties/types/{typeId}` | Get property type | **implemented** | `orders.get_property_type` |
| PUT | `/rest/orders/properties/types/{typeId}` | Update property type | **implemented** | `orders.update_property_type` |
| DELETE | `/rest/orders/properties/{id}` | Delete property of an order by property ID | **implemented** (deprecated by PlentyMarkets, use `PUT /rest/orders/{orderId}`) | `orders.delete_order_property` |
| PUT | `/rest/orders/properties/{id}` | Update property of an order by property ID | **implemented** (deprecated by PlentyMarkets, use `PUT /rest/orders/{orderId}`) | `orders.update_order_property` |
| GET | `/rest/orders/referrers` | List referrers | planned | — |
| GET | `/rest/orders/referrers/next_free_main` | Get next free main referrer ID | planned | — |
| GET | `/rest/orders/referrers/search` | Search for referrers | planned | — |
| POST | `/rest/orders/referrers/{parentReferrerId?}` | Create an order referrer | planned | — |
| DELETE | `/rest/orders/referrers/{referrerId}` | Delete referrer | planned | — |
| GET | `/rest/orders/referrers/{referrerId}` | Get a referrer | planned | — |
| PUT | `/rest/orders/referrers/{referrerId}` | Update referrer | planned | — |
| GET | `/rest/orders/search` | Search orders | **implemented** | `orders.search` |
| POST | `/rest/orders/search` | Search orders | **implemented** | `orders.search` |
| GET | `/rest/orders/shipping/active_shipping_service_providers` | Get the list of active shipping service providers for registration | planned | — |
| GET | `/rest/orders/shipping/countries` | List shipping countries | planned | — |
| GET | `/rest/orders/shipping/list_shipping_information` | Return paginated list containing orders with shipping information | planned | — |
| GET | `/rest/orders/shipping/package_types` | List shipping package types | planned | — |
| GET | `/rest/orders/shipping/package_types/{shippingPackageTypeId}` | Get a shipping package type | planned | — |
| DELETE | `/rest/orders/shipping/packages/items/{id}` | Delete package, variation or quantity for an order | planned | — |
| PUT | `/rest/orders/shipping/packages/items/{id}` | Update package, variation or quantity for an order | planned | — |
| DELETE | `/rest/orders/shipping/packages/items/{packageId}/{itemId}/{variationId}` | Delete items of an order package | planned | — |
| PUT | `/rest/orders/shipping/packages/items/{packageId}/{itemId}/{variationId}` | Update items of an order package | planned | — |
| PUT | `/rest/orders/shipping/packages/{orderShippingPackageId}` | Update an order shipping package by the packageId | planned | — |
| GET | `/rest/orders/shipping/packages/{packageId}/items` | List items of an order package | planned | — |
| POST | `/rest/orders/shipping/packages/{packageId}/items` | Create package, variation or quantity for an order | planned | — |
| GET | `/rest/orders/shipping/packages/{packageId}/packed_items` | Get packed items in a package | planned | — |
| GET | `/rest/orders/shipping/pallets` | List order shipping pallets | planned | — |
| POST | `/rest/orders/shipping/pallets` | Create order shipping pallets | planned | — |
| DELETE | `/rest/orders/shipping/pallets/{palletId}` | Delete all pallets of an order | planned | — |
| GET | `/rest/orders/shipping/pallets/{palletId}` | List all pallets of an order | planned | — |
| PUT | `/rest/orders/shipping/pallets/{palletId}` | Update all pallets of an order | planned | — |
| GET | `/rest/orders/shipping/pallets/{palletId}/packages` | Get all the packages for the given pallet ID | planned | — |
| GET | `/rest/orders/shipping/parcel_service_regions/{parcelServiceRegionId}` | Get an  order parcel service region | planned | — |
| GET | `/rest/orders/shipping/parcels/preview/{language?}` | Get preview list | planned | — |
| GET | `/rest/orders/shipping/presets` | List shipping profiles | planned | — |
| GET | `/rest/orders/shipping/presets/preview/{language?}` | Get preview list | planned | — |
| GET | `/rest/orders/shipping/presets/{presetId}` | Get a shipping profile | planned | — |
| GET | `/rest/orders/shipping/presets/{presetId}/parcel_service_regions` | List parcel service regions by parcel service preset ID | planned | — |
| GET | `/rest/orders/shipping/returns/returns_service_providers` | List returns service providers | planned | — |
| GET | `/rest/orders/shipping/returns/returns_service_providers/plugins` | List returns service provider plugins | planned | — |
| GET | `/rest/orders/shipping/returns/returns_service_providers/{providerId}` | Get returns service provider by the ID | planned | — |
| GET | `/rest/orders/shipping/shipping_information` | List orders with shipping information | planned | — |
| POST | `/rest/orders/shipping/shipping_information` | Create shipping information | planned | — |
| GET | `/rest/orders/shipping/shipping_service_providers` | List shipping service providers | planned | — |
| POST | `/rest/orders/shipping/shipping_service_providers` | Save a shipping service provider | planned | — |
| GET | `/rest/orders/shipping/shipping_service_providers/plugins` | List shipping service provider plugins | planned | — |
| GET | `/rest/orders/shipping/shipping_service_providers/{shipping_service_provider_id}` | Get a shipping service provider | planned | — |
| GET | `/rest/orders/status-history` | List status histories of orders | **implemented** | `orders.list_status_history` |
| GET | `/rest/orders/statuses` | Searches for order statuses | **implemented** | `orders.list_status_definitions` |
| POST | `/rest/orders/statuses` | Creates an order status. | **implemented** | `orders.create_status_definition` |
| GET | `/rest/orders/statuses/all` | Get all order statuses | **implemented** | `orders.list_all_status_definitions` |
| POST | `/rest/orders/statuses/group_functions` | Change order status properties | **implemented** | `orders.update_status_definition_properties` |
| DELETE | `/rest/orders/statuses/{statusId}` | Delete an order status | **implemented** | `orders.delete_status_definition` |
| GET | `/rest/orders/statuses/{statusId}` | Get an order status | **implemented** | `orders.get_status_definition` |
| PUT | `/rest/orders/statuses/{statusId}` | Update an order status | **implemented** | `orders.rename_status_definition` |
| DELETE | `/rest/orders/{orderId}` | Delete an order | **implemented** | `orders.delete` |
| GET | `/rest/orders/{orderId}` | Get an order | **implemented** | `orders.get` |
| PUT | `/rest/orders/{orderId}` | Update an order | **implemented** | `orders.update_status` |
| POST | `/rest/orders/{orderId}/advance_orders` | Create an advance order from a parent order | planned | — |
| PUT | `/rest/orders/{orderId}/advance_orders/convert` | Convert a sales order into an advance order | planned | — |
| POST | `/rest/orders/{orderId}/booking` | Book an order in | **implemented** | `orders.book_order_in` |
| PUT | `/rest/orders/{orderId}/cancel` | Cancel an order | **implemented** | `orders.cancel` |
| GET | `/rest/orders/{orderId}/contactWish` | Get a contact wish | **implemented** | `orders.get_contact_wish` |
| POST | `/rest/orders/{orderId}/coupons/{coupon}` | Redeem a coupon code | planned | — |
| POST | `/rest/orders/{orderId}/coupons/{coupon}/validate` | Validate coupon for order | planned | — |
| POST | `/rest/orders/{orderId}/credit_notes` | Create a credit note from a parent order | planned | — |
| POST | `/rest/orders/{orderId}/credit_notes/validate` | Validate order items for create a credit note from a parent order | planned | — |
| PUT | `/rest/orders/{orderId}/currency` | Update the order currency | **implemented** | `orders.update_order_currency` |
| GET | `/rest/orders/{orderId}/dates` | List all dates of an order | **implemented** | `orders.list_order_dates` |
| GET | `/rest/orders/{orderId}/dates/{typeId}` | Get a date | **implemented** | `orders.get_order_date` |
| POST | `/rest/orders/{orderId}/delivery_orders` | Create a delivery order from a parent order | planned | — |
| POST | `/rest/orders/{orderId}/delivery_orders/automatic` | Create delivery orders automatically for all order items | planned | — |
| POST | `/rest/orders/{orderId}/delivery_orders/validate` | Validate order items for create a delivery order from a parent order | planned | — |
| GET | `/rest/orders/{orderId}/family` | Get information about the order family | **implemented** | `orders.get_family` |
| GET | `/rest/orders/{orderId}/items` | Search order items | **implemented** | `orders.list_order_items` |
| POST | `/rest/orders/{orderId}/items/reorders/generate` | Create / update reorder(s) for order items | **implemented** | `orders.generate_order_item_reorders` |
| GET | `/rest/orders/{orderId}/items/serialNumbers` | List serial numbers of an order | **implemented** | `orders.list_order_serial_numbers` |
| POST | `/rest/orders/{orderId}/items/warehouse_locations/attach` | Attach warehouse locations. | **implemented** | `orders.attach_order_item_warehouse_locations` |
| POST | `/rest/orders/{orderId}/items/warehouse_locations/detach` | Detach warehouse locations. | **implemented** | `orders.detach_order_item_warehouse_locations` |
| DELETE | `/rest/orders/{orderId}/items/{orderItemId}` | Delete an order item | **implemented** | `orders.delete_order_item` |
| GET | `/rest/orders/{orderId}/items/{orderItemId}/serialNumbers` | List serial numbers of an order item | **implemented** | `orders.list_order_item_serial_numbers` |
| POST | `/rest/orders/{orderId}/items/{orderItemId}/serialNumbers` | Create item serial number and bind it to order item | **implemented** | `orders.create_order_item_serial_number` |
| GET | `/rest/orders/{orderId}/my_account_url` | Get My Account url of the order | **implemented** | `orders.get_my_account_url` |
| POST | `/rest/orders/{orderId}/offers` | Create an offer from a parent order | planned | — |
| DELETE | `/rest/orders/{orderId}/outgoing_stocks` | Revert outgoing stock | **implemented** | `orders.revert_order_outgoing_stock` |
| POST | `/rest/orders/{orderId}/outgoing_stocks` | Book out order items | **implemented** | `orders.book_out_order_items` |
| GET | `/rest/orders/{orderId}/packagenumbers` | List package numbers of an order | **implemented** | `orders.list_order_package_numbers` |
| POST | `/rest/orders/{orderId}/properties` | Create property for an order | **implemented** (deprecated by PlentyMarkets, use `PUT /rest/orders/{orderId}`) | `orders.create_order_property` |
| GET | `/rest/orders/{orderId}/properties/{typeId?}` | List properties of an order | **implemented** (deprecated by PlentyMarkets, use `GET /rest/orders/{orderId}`) | `orders.list_order_properties` |
| DELETE | `/rest/orders/{orderId}/properties/{typeId}` | Delete property of an order by order ID and property type ID | **implemented** (deprecated by PlentyMarkets, use `PUT /rest/orders/{orderId}`) | `orders.delete_order_property_by_type` |
| PUT | `/rest/orders/{orderId}/properties/{typeId}` | Update property of an order by order ID and property ID | **implemented** (deprecated by PlentyMarkets, use `PUT /rest/orders/{orderId}`) | `orders.update_order_property_by_type` |
| POST | `/rest/orders/{orderId}/redistributions` | Create a redistribution from a parent order | planned | — |
| POST | `/rest/orders/{orderId}/reorders` | Create a reorder from a parent order | **implemented** | `orders.create_order_reorder` |
| POST | `/rest/orders/{orderId}/reorders/generate` | Create reorder(s) for an order | **implemented** | `orders.generate_order_reorders` |
| POST | `/rest/orders/{orderId}/reorders/generate/validate` | Validate order items for create a reorder from a sales order, delivery order, repair and warranty | **implemented** | `orders.validate_order_reorders` |
| POST | `/rest/orders/{orderId}/repairs` | Create a repair order from a parent order | planned | — |
| POST | `/rest/orders/{orderId}/repairs/validate` | Validate order items for create a repair from a parent order | planned | — |
| POST | `/rest/orders/{orderId}/returns` | Create a return from a parent order | planned | — |
| POST | `/rest/orders/{orderId}/returns/validate` | Validate order items for create a return from a parent order | planned | — |
| POST | `/rest/orders/{orderId}/sales_orders` | Create a sales order from a parent order | planned | — |
| PUT | `/rest/orders/{orderId}/sales_orders/convert` | Convert an advance order into a sales order | planned | — |
| POST | `/rest/orders/{orderId}/sales_orders/validate` | Validate order items for create a sales order from a parent order | planned | — |
| DELETE | `/rest/orders/{orderId}/shipping/cancel_shipment` | Cancel a shipment | planned | — |
| DELETE | `/rest/orders/{orderId}/shipping/packages` | Delete all order shipping packages for an order | planned | — |
| GET | `/rest/orders/{orderId}/shipping/packages` | List order shipping packages | planned | — |
| POST | `/rest/orders/{orderId}/shipping/packages` | Create an order shipping package | planned | — |
| GET | `/rest/orders/{orderId}/shipping/packages/items` | List items contained in packages of an order | planned | — |
| GET | `/rest/orders/{orderId}/shipping/packages/packed_items` | List packed items of a shipping package by the order ID | planned | — |
| GET | `/rest/orders/{orderId}/shipping/packages/unpacked_items` | List unpacked items of a shipping package by the order ID | planned | — |
| GET | `/rest/orders/{orderId}/shipping/packages/unpacked_items_paginated` | List unpacked items from an order | planned | — |
| DELETE | `/rest/orders/{orderId}/shipping/packages/{orderShippingPackageId}` | Delete an order shipping package | planned | — |
| GET | `/rest/orders/{orderId}/shipping/packages/{orderShippingPackageId}` | Get an order shipping package | planned | — |
| PUT | `/rest/orders/{orderId}/shipping/packages/{orderShippingPackageId}` | Update an order shipping package | planned | — |
| GET | `/rest/orders/{orderId}/shipping/packages_paginated` | Get all the packages for the given order | planned | — |
| GET | `/rest/orders/{orderId}/shipping/pallets/packages/items` | List items contained in package pallets of an order | planned | — |
| DELETE | `/rest/orders/{orderId}/shipping/pallets/{palletId}/packages` | Delete all order shipping packages in a pallet | planned | — |
| GET | `/rest/orders/{orderId}/shipping/pallets/{palletId}/packages` | List all packages contained in pallets of an order | planned | — |
| PUT | `/rest/orders/{orderId}/shipping/pallets/{palletId}/packages` | Update all packages in a pallet | planned | — |
| POST | `/rest/orders/{orderId}/shipping/register_shipment` | Register a shipment | planned | — |
| DELETE | `/rest/orders/{orderId}/shipping/reset_shipment` | Reset a shipment | planned | — |
| DELETE | `/rest/orders/{orderId}/shipping/shipping_information` | Delete shipping information | planned | — |
| GET | `/rest/orders/{orderId}/shipping/shipping_information` | Get shipping information | planned | — |
| PUT | `/rest/orders/{orderId}/shipping/shipping_information/additional_data` | Update additional data of the shipping information | planned | — |
| GET | `/rest/orders/{orderId}/shipping/shipping_information/export_label` | Get Export label | planned | — |
| PUT | `/rest/orders/{orderId}/shipping/shipping_information/status` | Update the shipping status of the shipping information | planned | — |
| GET | `/rest/orders/{orderId}/status-history` | Get the status history of an order | **implemented** | `orders.get_order_status_history` |
| POST | `/rest/orders/{orderId}/subscriptions` | Create a subscription from a parent order | planned | — |
| POST | `/rest/orders/{orderId}/subscriptions/validate` | Validate order items for subscription creation from a parent order | planned | — |
| POST | `/rest/orders/{orderId}/transactions` | Create order item transactions for an order | **implemented** | `orders.create_order_transactions` |
| POST | `/rest/orders/{orderId}/warranties` | Create a warranty from a parent order | planned | — |
| POST | `/rest/orders/{orderId}/warranties/validate` | Validate order items for create a warranty from a parent order | planned | — |
| POST | `/rest/redistributions` | Create a redistribution | planned | — |
| POST | `/rest/redistributions/preview` | Get a redistribution create preview. | planned | — |
| DELETE | `/rest/redistributions/{orderId}` | Delete a redistribution | planned | — |
| PUT | `/rest/redistributions/{orderId}` | Update a redistribution | planned | — |
| POST | `/rest/redistributions/{orderId}/book` | Book an order in | planned | — |
| PUT | `/rest/redistributions/{orderId}/preview` | Get a redistribution update preview | planned | — |
| POST | `/rest/reorders` | Create a reorder | planned | — |
| POST | `/rest/reorders/preview` | Get a reorder create preview. | planned | — |
| DELETE | `/rest/reorders/{orderId}` | Delete a reorder | planned | — |
| PUT | `/rest/reorders/{orderId}` | Update a reorder | planned | — |
| POST | `/rest/reorders/{orderId}/book` | Book an order in | planned | — |
| PUT | `/rest/reorders/{orderId}/currency` | Update the currency | planned | — |
| GET | `/rest/reorders/{orderId}/delivery_date` | Get the delivery date | planned | — |
| PUT | `/rest/reorders/{orderId}/delivery_dates` | Calculate and save the delivery dates | planned | — |
| PUT | `/rest/reorders/{orderId}/preview` | Get a reorder update preview | planned | — |
| POST | `/rest/repairs` | Create a repair | planned | — |
| POST | `/rest/repairs/items/{orderItemId}/assign_variation` | Change an order item of type "unassigned variation" to "variation". | planned | — |
| POST | `/rest/repairs/items/{orderItemId}/unassign_variation` | Change an order item of type "variation" to "unassigned variation". | planned | — |
| POST | `/rest/repairs/preview` | Get a repair order create preview. | planned | — |
| GET | `/rest/repairs/reasons` | Get all order repair reasons | planned | — |
| POST | `/rest/repairs/reasons` | Set an order repair reason | planned | — |
| DELETE | `/rest/repairs/reasons/{repairReasonId}` | Delete an order repair reason | planned | — |
| GET | `/rest/repairs/reasons/{repairReasonId}` | Get an order repair reason | planned | — |
| GET | `/rest/repairs/status` | Get all order repair status | planned | — |
| POST | `/rest/repairs/status` | Set an order repair status | planned | — |
| DELETE | `/rest/repairs/status/{repairStatusId}` | Delete an order repair status | planned | — |
| GET | `/rest/repairs/status/{repairStatusId}` | Get an order repair status | planned | — |
| DELETE | `/rest/repairs/{orderId}` | Delete a repair | planned | — |
| PUT | `/rest/repairs/{orderId}` | Update a repair | planned | — |
| POST | `/rest/repairs/{orderId}/book` | Book out order items | planned | — |
| POST | `/rest/repairs/{orderId}/cancel_booking` | Revert outgoing stock | planned | — |
| POST | `/rest/repairs/{orderId}/cancel_booking/validate` | Validate cancellation of the booking of an order | planned | — |
| PUT | `/rest/repairs/{orderId}/preview` | Get a repair order update preview | planned | — |
| POST | `/rest/returns` | Create a return | planned | — |
| POST | `/rest/returns/items/{orderItemId}/assign_variation` | Change an order item of type "unassigned variation" to "variation". | planned | — |
| POST | `/rest/returns/items/{orderItemId}/unassign_variation` | Change an order item of type "variation" to "unassigned variation". | planned | — |
| POST | `/rest/returns/preview` | Get a return create preview. | planned | — |
| GET | `/rest/returns/reasons` | Get all order return reasons | planned | — |
| POST | `/rest/returns/reasons` | Set an order return reason | planned | — |
| DELETE | `/rest/returns/reasons/{returnReasonsId}` | Delete an order return reason | planned | — |
| GET | `/rest/returns/reasons/{returnReasonsId}` | Get an order return reason | planned | — |
| GET | `/rest/returns/status` | Get all order return status | planned | — |
| POST | `/rest/returns/status` | Set an order return status | planned | — |
| DELETE | `/rest/returns/status/{returnStatusId}` | Delete an order return status | planned | — |
| GET | `/rest/returns/status/{returnStatusId}` | Get an order return status | planned | — |
| DELETE | `/rest/returns/{orderId}` | Delete a return | planned | — |
| PUT | `/rest/returns/{orderId}` | Update a return | planned | — |
| POST | `/rest/returns/{orderId}/book` | Book order items of return | planned | — |
| POST | `/rest/returns/{orderId}/book/validate` | Validate booking of an return | planned | — |
| PUT | `/rest/returns/{orderId}/preview` | Get a return update preview | planned | — |
| POST | `/rest/sales_orders` | Create a sales order | planned | — |
| POST | `/rest/sales_orders/group` | Group multiple orders in one order. | planned | — |
| POST | `/rest/sales_orders/incomplete/preview` | Get a sales order create incomplete preview. | planned | — |
| POST | `/rest/sales_orders/items/{orderItemId}/assign_variation` | Change an order item of type "unassigned variation" to "variation". | planned | — |
| POST | `/rest/sales_orders/items/{orderItemId}/unassign_variation` | Change an order item of type "variation" to "unassigned variation". | planned | — |
| POST | `/rest/sales_orders/preview` | Get a sales order create preview. | planned | — |
| DELETE | `/rest/sales_orders/{orderId}` | Delete a sales order | planned | — |
| PUT | `/rest/sales_orders/{orderId}` | Update a sales order | planned | — |
| POST | `/rest/sales_orders/{orderId}/book` | Book out order items | planned | — |
| POST | `/rest/sales_orders/{orderId}/cancel_booking` | Revert outgoing stock | planned | — |
| POST | `/rest/sales_orders/{orderId}/cancel_booking/validate` | Validate cancellation of the booking of an order | planned | — |
| PUT | `/rest/sales_orders/{orderId}/preview` | Get a sales order update preview. | planned | — |
| POST | `/rest/sales_orders/{orderId}/split` | Split a sales order into at least two sales orders | planned | — |
| DELETE | `/rest/shipping_center/reset_shipments` | Reset a shipment | planned | — |
| POST | `/rest/subscriptions` | Create a subscription | planned | — |
| POST | `/rest/subscriptions/preview` | Get a subscription create preview. | planned | — |
| DELETE | `/rest/subscriptions/{orderId}` | Delete a subscription | planned | — |
| PUT | `/rest/subscriptions/{orderId}` | Update a subscription | planned | — |
| PUT | `/rest/subscriptions/{orderId}/currency` | Update the currency | planned | — |
| POST | `/rest/subscriptions/{orderId}/manual_run` | Create an order for today for a given subscription. | planned | — |
| PUT | `/rest/subscriptions/{orderId}/preview` | Get a subscription update preview | planned | — |
| GET | `/rest/system/settings/taric_vat_assignment` | List taric vat assignments | planned | — |
| DELETE | `/rest/system/settings/taric_vat_assignment/{taricCode}/{countryId}` | Delete taric vat assignment | planned | — |
| GET | `/rest/system/settings/taric_vat_assignment/{taricCode}/{countryId}` | Get taric vat assignment | planned | — |
| POST | `/rest/system/settings/taric_vat_assignment/{taricCode}/{countryId}` | Create taric vat assignment | planned | — |
| PUT | `/rest/system/settings/taric_vat_assignment/{taricCode}/{countryId}` | Update taric vat assignment | planned | — |
| POST | `/rest/warranties` | Create a warranty | planned | — |
| POST | `/rest/warranties/items/{orderItemId}/assign_variation` | Change an order item of type "unassigned variation" to "variation". | planned | — |
| POST | `/rest/warranties/items/{orderItemId}/unassign_variation` | Change an order item of type "variation" to "unassigned variation". | planned | — |
| POST | `/rest/warranties/preview` | Get a warranty create preview. | planned | — |
| DELETE | `/rest/warranties/{orderId}` | Delete a warranty | planned | — |
| PUT | `/rest/warranties/{orderId}` | Update a warranty | planned | — |
| POST | `/rest/warranties/{orderId}/book` | Book out order items | planned | — |
| POST | `/rest/warranties/{orderId}/cancel_booking` | Revert outgoing stock | planned | — |
| POST | `/rest/warranties/{orderId}/cancel_booking/validate` | Validate cancellation of the booking of an order | planned | — |
| PUT | `/rest/warranties/{orderId}/preview` | Get a warranty update preview | planned | — |

#### Known Schema Gaps

The following `OrdersModule` methods accept `data: dict[str, Any]` because
PlentyMarkets' published OpenAPI spec declares no request body schema at all
for these endpoints — not even an empty placeholder object. The payload
shape below is inferred from field names, sibling schemas, and endpoint
descriptions only; each method's docstring carries the same caveat. Verify
against a live system and tighten to a proper `TypedDict` once confirmed.

| Method | Endpoint | Note |
|---|---|---|
| `orders.create_order_item_serial_number` | `POST /rest/orders/{orderId}/items/{orderItemId}/serialNumbers` | Likely just `serialNumber` (string), possibly with an `identification`-style field. |
| `orders.attach_order_item_warehouse_locations` | `POST /rest/orders/{orderId}/items/warehouse_locations/attach` | Likely a list of order-item-to-warehouse-location mappings. |
| `orders.detach_order_item_warehouse_locations` | `POST /rest/orders/{orderId}/items/warehouse_locations/detach` | Likely the same shape as `attach`. |
| `orders.generate_order_item_reorders` | `POST /rest/orders/{orderId}/items/reorders/generate` | Likely order item IDs and/or quantities to reorder. |
| `orders.create_order_reorder` | `POST /rest/orders/{orderId}/reorders` | Spec description: "parent order ID and quantities to use must be specified" — exact key names unknown. |
| `orders.generate_order_reorders` | `POST /rest/orders/{orderId}/reorders/generate` | Order-scoped sibling of `generate_order_item_reorders`; likely the same shape. |
| `orders.validate_order_reorders` | `POST /rest/orders/{orderId}/reorders/generate/validate` | Likely the same shape as `create_order_reorder`/`generate_order_reorders`, used for pre-flight validation. |

### `OrderSummary`

0/8 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/accounts/order_summaries` | List order summaries | planned | — |
| POST | `/rest/accounts/order_summaries` | Create order summary | planned | — |
| GET | `/rest/accounts/order_summaries/contacts/{contactId}` | Get order summary by contact ID | planned | — |
| GET | `/rest/accounts/order_summaries/orders/{addressId}` | Get order summary by address ID | planned | — |
| GET | `/rest/accounts/order_summaries/unpaid` | List unpaid order summaries | planned | — |
| DELETE | `/rest/accounts/order_summaries/{orderSummaryId}` | Delete order summary | planned | — |
| GET | `/rest/accounts/order_summaries/{orderSummaryId}` | Get order summary by order summary ID | planned | — |
| PUT | `/rest/accounts/order_summaries/{orderSummaryId}` | Update order summary | planned | — |

### `Payment`

0/52 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| POST | `/rest/payment/properties/types/names` | Create name of property type | planned | — |
| PUT | `/rest/payment/properties/types/names` | Update name of property type | planned | — |
| GET | `/rest/payment/properties/types/names/{lang?}` | List names of property types | planned | — |
| GET | `/rest/payment/properties/types/names/{nameId}` | Get a name of a property type | planned | — |
| DELETE | `/rest/payment/{paymentId}/contact` | Delete Payment-Contact-Relation | planned | — |
| POST | `/rest/payment/{paymentId}/contact/{contactId}` | Create Payment-Contact-Relation | planned | — |
| DELETE | `/rest/payment/{paymentId}/order` | Delete Payment-Order-Relation | planned | — |
| POST | `/rest/payment/{paymentId}/order/{invoiceNumber}/invoice` | Create order relation with validation | planned | — |
| POST | `/rest/payment/{paymentId}/order/{orderId}` | Create Payment-Order-Relation | planned | — |
| POST | `/rest/payment/{paymentId}/order/{orderId}/validation` | Create order relation with validation | planned | — |
| GET | `/rest/payments` | List payments | planned | — |
| POST | `/rest/payments` | Create a payment | planned | — |
| PUT | `/rest/payments` | Update a payment | planned | — |
| DELETE | `/rest/payments/bulk` | Delete payents | planned | — |
| GET | `/rest/payments/entrydate` | List payments by entry date | planned | — |
| GET | `/rest/payments/importdate` | List payments by import date | planned | — |
| GET | `/rest/payments/methodNames` | List payment methods names | planned | — |
| GET | `/rest/payments/methodNames/{paymentMethodId}` | List all payment method names for a payment method id | planned | — |
| GET | `/rest/payments/methodNames/{paymentMethodId}/{lang}` | Gets a payment method name by id and lang | planned | — |
| GET | `/rest/payments/methods` | List payment methods | planned | — |
| POST | `/rest/payments/methods` | Create a payment method | planned | — |
| PUT | `/rest/payments/methods` | Update a payment method | planned | — |
| PUT | `/rest/payments/methods/bulk` | Updates payment methods | planned | — |
| GET | `/rest/payments/methods/list` | Get payment methods | planned | — |
| GET | `/rest/payments/methods/list/backend_active/{language}` | Get active payment methods | planned | — |
| GET | `/rest/payments/methods/list/backend_icon` | Get payment methods and icons | planned | — |
| GET | `/rest/payments/methods/list/backend_searchable/{language}` | Get searchable payment methods | planned | — |
| GET | `/rest/payments/methods/list/documentbuilder_active/{language}` | Get DocumenBuilder active payment methods | planned | — |
| GET | `/rest/payments/methods/list/handle_subscription/{language}` | Get subscriptions handling payment methods | planned | — |
| GET | `/rest/payments/methods/plugins/{pluginKey}` | Get a payment method | planned | — |
| GET | `/rest/payments/methods/preview/{language?}` | Get preview list for payment method | planned | — |
| GET | `/rest/payments/methods/{methodId}` | List payments of a payment method | planned | — |
| DELETE | `/rest/payments/order/{orderId}` | Detach all the payment from and order. | planned | — |
| POST | `/rest/payments/orders/autoassign/bulk` | Assign Payments | planned | — |
| GET | `/rest/payments/orders/{orderId}` | List payments of an order | planned | — |
| GET | `/rest/payments/properties` | List properties | planned | — |
| POST | `/rest/payments/properties` | Create property | planned | — |
| PUT | `/rest/payments/properties` | Update property | planned | — |
| GET | `/rest/payments/properties/date` | List properties by creation date | planned | — |
| GET | `/rest/payments/properties/types` | List property types | planned | — |
| POST | `/rest/payments/properties/types` | Create property type | planned | — |
| PUT | `/rest/payments/properties/types` | Update property type | planned | — |
| GET | `/rest/payments/properties/types/{typeId}` | Get a property type | planned | — |
| GET | `/rest/payments/properties/{propertyId}` | Get a property | planned | — |
| GET | `/rest/payments/property/{propertyTypeId}/{propertyValue}` | List payments by property type ID and value | planned | — |
| GET | `/rest/payments/search` | Search payments | planned | — |
| POST | `/rest/payments/search` | Search payments | planned | — |
| GET | `/rest/payments/status/{statusId}` | List payments of a payment status | planned | — |
| GET | `/rest/payments/transactions/{transactionTypeId}` | List payments of a transaction type | planned | — |
| DELETE | `/rest/payments/{paymentId}` | Delete payment | planned | — |
| GET | `/rest/payments/{paymentId}` | Get a payment | planned | — |
| GET | `/rest/payments/{paymentId}/properties` | List properties for a payment | planned | — |

### `Pim`

80/80 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/pim/amazon-product-types` | Get item amazon product types | **implemented** | `pim.list_amazon_product_types` |
| DELETE | `/rest/pim/attributes` | Delete a list of attributes | **implemented** | `pim.delete_attributes` |
| GET | `/rest/pim/attributes` | Search for attributes | **implemented** | `pim.list_attributes` |
| POST | `/rest/pim/attributes` | Create a list of attributes | **implemented** | `pim.create_attributes` |
| PUT | `/rest/pim/attributes` | Update a list of attributes | **implemented** | `pim.update_attributes` |
| DELETE | `/rest/pim/attributes/names` | Delete a list of attribute names | **implemented** | `pim.delete_attribute_names` |
| GET | `/rest/pim/attributes/names` | Search attribute names | **implemented** | `pim.list_attribute_names` |
| POST | `/rest/pim/attributes/names` | Create a list of attribute names | **implemented** | `pim.create_attribute_names` |
| PUT | `/rest/pim/attributes/names` | Update a list of attribute names | **implemented** | `pim.update_attribute_names` |
| DELETE | `/rest/pim/attributes/values` | Delete a list of attribute values | **implemented** | `pim.delete_attribute_values` |
| GET | `/rest/pim/attributes/values` | Search attribute values | **implemented** | `pim.list_attribute_values` |
| POST | `/rest/pim/attributes/values` | Create a list of attribute values | **implemented** | `pim.create_attribute_values` |
| PUT | `/rest/pim/attributes/values` | Update a list of attribute values | **implemented** | `pim.update_attribute_values` |
| DELETE | `/rest/pim/attributes/values/names` | Delete a list of attribute value names | **implemented** | `pim.delete_attribute_value_names` |
| GET | `/rest/pim/attributes/values/names` | Search attribute value names | **implemented** | `pim.list_attribute_value_names` |
| POST | `/rest/pim/attributes/values/names` | Create a list of attribute value names | **implemented** | `pim.create_attribute_value_names` |
| PUT | `/rest/pim/attributes/values/names` | Update a list of attribute value names | **implemented** | `pim.update_attribute_value_names` |
| GET | `/rest/pim/attributes/values/{id}` | Get one attribute value | **implemented** | `pim.get_attribute_value` |
| GET | `/rest/pim/attributes/{id}` | Get one attribute | **implemented** | `pim.get_attribute` |
| DELETE | `/rest/pim/barcodes` | Delete a list of barcodes | **implemented** | `pim.delete_barcodes` |
| GET | `/rest/pim/barcodes` | Search for barcodes | **implemented** | `pim.list_barcodes` |
| POST | `/rest/pim/barcodes` | Create a list of barcodes | **implemented** | `pim.create_barcodes` |
| PUT | `/rest/pim/barcodes` | Update a list of barcodes | **implemented** | `pim.update_barcodes` |
| GET | `/rest/pim/barcodes/duplicates` | Get all barcode duplicates | **implemented** | `pim.list_barcode_duplicates` |
| GET | `/rest/pim/barcodes/duplicates/count` | Get barcode duplicates | **implemented** | `pim.count_barcode_duplicates` |
| GET | `/rest/pim/barcodes/duplicates/settings` | List barcodes duplicate settings | **implemented** | `pim.get_barcode_duplicate_settings` |
| GET | `/rest/pim/categories` | Search categories | **implemented** | `pim.list_categories` |
| GET | `/rest/pim/categories/branches` | Search category branches | **implemented** | `pim.list_category_branches` |
| GET | `/rest/pim/categories/clients` | Search category clients | **implemented** | `pim.list_category_clients` |
| GET | `/rest/pim/categories/details` | Search category details | **implemented** | `pim.list_category_details` |
| GET | `/rest/pim/categories/properties` | Search category properties | **implemented** | `pim.list_category_properties` |
| GET | `/rest/pim/categories/{id}` | Get one category by given ID | **implemented** | `pim.get_category` |
| DELETE | `/rest/pim/item-serial-numbers` | Delete item serial numbers | **implemented** | `pim.delete_item_serial_numbers` |
| GET | `/rest/pim/item-serial-numbers` | Search for item serial numbers | **implemented** | `pim.list_item_serial_numbers` |
| POST | `/rest/pim/item-serial-numbers` | Create item serial numbers | **implemented** | `pim.create_item_serial_numbers` |
| PUT | `/rest/pim/item-serial-numbers` | Update item serial numbers | **implemented** | `pim.update_item_serial_numbers` |
| GET | `/rest/pim/items/{id}/attributes` | Get Attributes linked to given item | **implemented** | `pim.get_item_attributes` |
| GET | `/rest/pim/items/{id}/combinations` | Get all existing variation combinations for current item | **implemented** | `pim.get_item_combinations` |
| DELETE | `/rest/pim/sales_prices` | Delete a list of sales prices | **implemented** | `pim.delete_sales_prices` |
| GET | `/rest/pim/sales_prices` | Search for sales prices | **implemented** | `pim.list_sales_prices` |
| POST | `/rest/pim/sales_prices` | Create a list of sales prices | **implemented** | `pim.create_sales_prices` |
| PUT | `/rest/pim/sales_prices` | Update a list of sales prices | **implemented** | `pim.update_sales_prices` |
| GET | `/rest/pim/sales_prices/{id}` | Get one sales price by ID | **implemented** | `pim.get_sales_price` |
| DELETE | `/rest/pim/variations` | Delete a list of variations | **implemented** | `pim.delete_variations` |
| GET | `/rest/pim/variations` | List variations including the specified related data | **implemented** | `pim.list_variations` |
| PUT | `/rest/pim/variations` | Create a list of variations and their related data | **implemented** | `pim.create_variations` |
| DELETE | `/rest/pim/variations/additional_skus` | Delete a list of variation additional skus | **implemented** | `pim.delete_variation_additional_skus` |
| PUT | `/rest/pim/variations/additional_skus` | Create and update variation additional skus | **implemented** | `pim.update_variation_additional_skus` |
| DELETE | `/rest/pim/variations/barcodes` | Delete variation barcodes | **implemented** | `pim.delete_variation_barcodes` |
| PUT | `/rest/pim/variations/barcodes` | Create and update a list of variation barcodes | **implemented** | `pim.update_variation_barcodes` |
| PUT | `/rest/pim/variations/bases` | Create and update a list of variations | **implemented** | `pim.update_variation_bases` |
| DELETE | `/rest/pim/variations/bundle_components` | Delete variation bundle components | **implemented** | `pim.delete_variation_bundle_components` |
| PUT | `/rest/pim/variations/bundle_components` | Create and update a list of variation bundle components | **implemented** | `pim.update_variation_bundle_components` |
| DELETE | `/rest/pim/variations/categories` | Delete variation categories | **implemented** | `pim.delete_variation_categories` |
| PUT | `/rest/pim/variations/categories` | Create and update a list of variation categories | **implemented** | `pim.update_variation_categories` |
| DELETE | `/rest/pim/variations/clients` | Delete a list of variation clients | **implemented** | `pim.delete_variation_clients` |
| PUT | `/rest/pim/variations/clients` | Create a list of variation clients | **implemented** | `pim.update_variation_clients` |
| DELETE | `/rest/pim/variations/comments` | Delete variation comments | **implemented** | `pim.delete_variation_comments` |
| PUT | `/rest/pim/variations/comments` | Create and update a list of variation comments | **implemented** | `pim.update_variation_comments` |
| DELETE | `/rest/pim/variations/default_categories` | Delete variation default categories | **implemented** | `pim.delete_variation_default_categories` |
| PUT | `/rest/pim/variations/default_categories` | Create and update a list of variation default categories | **implemented** | `pim.update_variation_default_categories` |
| DELETE | `/rest/pim/variations/images` | Delete variation images | **implemented** | `pim.delete_variation_images` |
| PUT | `/rest/pim/variations/images` | Create a list of variation images | **implemented** | `pim.update_variation_images` |
| DELETE | `/rest/pim/variations/market_ident_numbers` | Delete a list of variation market ident numbers | **implemented** | `pim.delete_variation_market_ident_numbers` |
| PUT | `/rest/pim/variations/market_ident_numbers` | Create and update a list of variation market ident numbers | **implemented** | `pim.update_variation_market_ident_numbers` |
| DELETE | `/rest/pim/variations/markets` | Delete a list of variation markets | **implemented** | `pim.delete_variation_markets` |
| PUT | `/rest/pim/variations/markets` | Create a list of variation markets | **implemented** | `pim.update_variation_markets` |
| DELETE | `/rest/pim/variations/properties` | Delete a list of variation properties | **implemented** | `pim.delete_variation_properties` |
| PUT | `/rest/pim/variations/properties` | Create and update a list of variation properties | **implemented** | `pim.update_variation_properties` |
| DELETE | `/rest/pim/variations/sales_prices` | Delete a list of variation sales prices | **implemented** | `pim.delete_variation_sales_prices` |
| PUT | `/rest/pim/variations/sales_prices` | Create and update a list of variation sales prices | **implemented** | `pim.update_variation_sales_prices` |
| GET | `/rest/pim/variations/scroll` | Get all variations, scrolled by a cursor | **implemented** | `pim.paginate_variations` |
| DELETE | `/rest/pim/variations/skus` | Delete a list of variation skus | **implemented** | `pim.delete_variation_skus` |
| PUT | `/rest/pim/variations/skus` | Create and update a list of variation skus | **implemented** | `pim.update_variation_skus` |
| DELETE | `/rest/pim/variations/supplier` | Delete a list of variation supplier | **implemented** | `pim.delete_variation_supplier` |
| PUT | `/rest/pim/variations/supplier` | Create and update a list of variation suppliers | **implemented** | `pim.update_variation_supplier` |
| DELETE | `/rest/pim/variations/tags` | Delete a list of variation tags | **implemented** | `pim.delete_variation_tags` |
| PUT | `/rest/pim/variations/tags` | Create a list of variation tags | **implemented** | `pim.update_variation_tags` |
| DELETE | `/rest/pim/variations/warehouses` | Delete a list of variation warehouses | **implemented** | `pim.delete_variation_warehouses` |
| PUT | `/rest/pim/variations/warehouses` | Create and update a list of variation warehouses | **implemented** | `pim.update_variation_warehouses` |

### `plentyMarketplace`

0/2 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| POST | `/rest/io/customer/login` | plentyMarketplace login | planned | — |
| POST | `/rest/partner-portal/partner-plugin/visibility` | Change plugin visibility | planned | — |

### `PluginMultilingualism`

0/5 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| POST | `/rest/languages/translations` | Create a new translation | planned | — |
| DELETE | `/rest/languages/translations/{translationId}` | Delete a translation | planned | — |
| GET | `/rest/languages/translations/{translationId}` | Get a translation | planned | — |
| PUT | `/rest/languages/translations/{translationId}` | Update a translation | planned | — |
| DELETE | `/rest/plugin_sets/{pluginSetId}/languages/{languageCode}` | Delete multiple translation | planned | — |

### `Plugins`

0/13 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/plugin_sets/{pluginSetId}/updateReversedDependencies` | Update reversed dependencies | planned | — |
| GET | `/rest/plugins` | List plugins | planned | — |
| POST | `/rest/plugins` | Create a plugin | planned | — |
| POST | `/rest/plugins/constraint/version` | Checks for version constraint | planned | — |
| GET | `/rest/plugins/search` | List plugins | planned | — |
| GET | `/rest/plugins/seo/sitemap` | Load sitemap patterns | planned | — |
| GET | `/rest/plugins/ui` | List plugins for backend UI | planned | — |
| DELETE | `/rest/plugins/{pluginId}` | Delete a plugin | planned | — |
| GET | `/rest/plugins/{pluginId}` | Get a plugin | planned | — |
| PUT | `/rest/plugins/{pluginId}` | Update a plugin | planned | — |
| DELETE | `/rest/plugins/{pluginId}/plugin_sets/{pluginSetId}` | Delete a plugin | planned | — |
| POST | `/rest/plugins/{pluginName}/plugin_sets/{pluginSetId}/reversedDependencies` | Get reversed requirements | planned | — |
| POST | `/rest/plugins_mail` | Send mail | planned | — |

### `PluginSet`

0/26 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/plugin_sets` | List all Sets | planned | — |
| POST | `/rest/plugin_sets` | Create a Set | planned | — |
| GET | `/rest/plugin_sets/info` | Get details about plugin sets | planned | — |
| GET | `/rest/plugin_sets/preview_hash` | Get the preview hash for a set | planned | — |
| GET | `/rest/plugin_sets/s3-inbox-opensource-plugins` | Get open source plugins from inbox | planned | — |
| GET | `/rest/plugin_sets/{pluginSetId}/languages` | List all the plugins translations for a plugin set | planned | — |
| GET | `/rest/plugin_sets/{pluginSetId}/languages/csv/{languageCode}` | List all plugin translations csv. | planned | — |
| POST | `/rest/plugin_sets/{pluginSetId}/languages/upload_translations` | Uploads and syncs resources | planned | — |
| GET | `/rest/plugin_sets/{pluginSetId}/languages/{targetLanguage}` | List all plugin translations merged. | planned | — |
| POST | `/rest/plugin_sets/{pluginSetId}/languages/{targetLanguage}` | Update all plugin translations | planned | — |
| DELETE | `/rest/plugin_sets/{setId}` | Delete a set | planned | — |
| GET | `/rest/plugin_sets/{setId}` | Get a set | planned | — |
| PUT | `/rest/plugin_sets/{setId}` | Update a set | planned | — |
| GET | `/rest/plugin_sets/{setId}/plugins` | List all Plugins of Set | planned | — |
| GET | `/rest/plugin_sets/{setId}/plugins/get_compatibility/{pluginName}/{variationId}` | Get plugin compatibility | planned | — |
| GET | `/rest/plugin_sets/{setId}/plugins/search` | Search plugins | planned | — |
| DELETE | `/rest/plugin_sets/{setId}/plugins/{pluginId}` | Remove a plugin from a set | planned | — |
| POST | `/rest/plugin_sets/{setId}/plugins/{pluginId}` | Add a plugin to a set | planned | — |
| PUT | `/rest/plugin_sets/{setId}/plugins/{pluginId}` | Change a plugin's 'active' status for a set. | planned | — |
| POST | `/rest/plugin_sets/{setId}/plugins/{pluginId}/install_git_plugin` | Install a git plugin into a set | planned | — |
| POST | `/rest/plugin_sets/{setId}/plugins/{pluginId}/setPosition` | Set a plugin's position in a set | planned | — |
| GET | `/rest/plugin_sets/{setId}/set_entries` | List all SetEntries of Set | planned | — |
| GET | `/rest/plugin_sets_new/git_plugin_details/{pluginName}` | Get git plugin description data | planned | — |
| GET | `/rest/plugin_sets_new/plugin_details/{pluginName}/{variationId}` | Get plugin description data | planned | — |
| GET | `/rest/plugins/plugin_sets/{pluginSetId}/plugins` | List all Plugins of Set | planned | — |
| GET | `/rest/plugins/{pluginId}/plugin_sets/{pluginSetId}/containers` | List containers | planned | — |

### `Property`

0/159 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/properties` | List properties | planned | — |
| POST | `/rest/properties` | Create a property | planned | — |
| GET | `/rest/properties/amazons` | List property amazons | planned | — |
| POST | `/rest/properties/amazons` | Create one or multiple property amazon | planned | — |
| PUT | `/rest/properties/amazons` | Update one or multiple property amazon | planned | — |
| DELETE | `/rest/properties/amazons/{propertyAmazonId}` | Delete a property amazon | planned | — |
| GET | `/rest/properties/amazons/{propertyAmazonId}` | Get a property amazon | planned | — |
| GET | `/rest/properties/availabilities` | List availabilities | planned | — |
| POST | `/rest/properties/availabilities` | Create an availability | planned | — |
| DELETE | `/rest/properties/availabilities/{availabilityId}` | Delete an availability | planned | — |
| GET | `/rest/properties/availabilities/{availabilityId}` | Get an availability | planned | — |
| PUT | `/rest/properties/availabilities/{availabilityId}` | Update an availability | planned | — |
| GET | `/rest/properties/destinations` | Get property destinations | planned | — |
| GET | `/rest/properties/groups` | List property groups | planned | — |
| POST | `/rest/properties/groups` | Create a property group | planned | — |
| GET | `/rest/properties/groups/names` | List group names | planned | — |
| POST | `/rest/properties/groups/names` | Create an group name | planned | — |
| DELETE | `/rest/properties/groups/names/{groupNameId}` | Delete a group name | planned | — |
| GET | `/rest/properties/groups/names/{groupNameId}` | Get a group name | planned | — |
| PUT | `/rest/properties/groups/names/{groupNameId}` | Update a group name | planned | — |
| GET | `/rest/properties/groups/options` | List group options | planned | — |
| POST | `/rest/properties/groups/options` | Create a group option | planned | — |
| DELETE | `/rest/properties/groups/options/{groupOptionId}` | Delete a group option | planned | — |
| GET | `/rest/properties/groups/options/{groupOptionId}` | Get a group option | planned | — |
| PUT | `/rest/properties/groups/options/{groupOptionId}` | Update a group option | planned | — |
| GET | `/rest/properties/groups/surcharge/types` | Get surcharge types from module configuration | planned | — |
| GET | `/rest/properties/groups/types` | Get group types from module configuration | planned | — |
| GET | `/rest/properties/groups/{groupId}` | Get a property group | planned | — |
| PUT | `/rest/properties/groups/{groupId}` | Update a property group | planned | — |
| POST | `/rest/properties/groups/{groupId}/properties` | Mass attach propertyId and groupId collection into the pivot table. | planned | — |
| DELETE | `/rest/properties/groups/{groupId}/properties/{propertyId}` | Detach a property from a property group. | planned | — |
| POST | `/rest/properties/groups/{groupId}/properties/{propertyId}` | Attach a property to a property group | planned | — |
| DELETE | `/rest/properties/groups/{propertyId}` | Delete a property group | planned | — |
| GET | `/rest/properties/markets` | List property markets | planned | — |
| POST | `/rest/properties/markets` | Create a property market | planned | — |
| DELETE | `/rest/properties/markets/{propertiesMarketId}` | Delete a property market | planned | — |
| GET | `/rest/properties/markets/{propertiesMarketId}` | Get a property market | planned | — |
| PUT | `/rest/properties/markets/{propertiesMarketId}` | Update a property market | planned | — |
| DELETE | `/rest/properties/multiple/options` | Delete property options | planned | — |
| POST | `/rest/properties/multiple/options` | Create property options | planned | — |
| GET | `/rest/properties/names` | List names | planned | — |
| POST | `/rest/properties/names` | Create a name | planned | — |
| DELETE | `/rest/properties/names/{nameId}` | Delete a property name | planned | — |
| GET | `/rest/properties/names/{nameId}` | Get a property name | planned | — |
| PUT | `/rest/properties/names/{nameId}` | Update a property name | planned | — |
| GET | `/rest/properties/options` | List property options | planned | — |
| POST | `/rest/properties/options` | Create a property option | planned | — |
| DELETE | `/rest/properties/options/{propertyOptionId}` | Delete a property option | planned | — |
| GET | `/rest/properties/options/{propertyOptionId}` | Get a property option | planned | — |
| PUT | `/rest/properties/options/{propertyOptionId}` | Update a property option | planned | — |
| DELETE | `/rest/properties/relations` | Delete property relations | planned | — |
| GET | `/rest/properties/relations` | List property relations | planned | — |
| POST | `/rest/properties/relations` | Create a property relation | planned | — |
| PUT | `/rest/properties/relations` | Update relations | planned | — |
| GET | `/rest/properties/relations/values` | List property relation values | planned | — |
| POST | `/rest/properties/relations/values` | Create a property relation value | planned | — |
| PUT | `/rest/properties/relations/values` | Update multiple property relation value | planned | — |
| DELETE | `/rest/properties/relations/values/{propertiesRelationValueId}` | Delete a property relation value | planned | — |
| GET | `/rest/properties/relations/values/{propertiesRelationValueId}` | Get a property relation value | planned | — |
| PUT | `/rest/properties/relations/values/{propertiesRelationValueId}` | Update a property relation value | planned | — |
| DELETE | `/rest/properties/relations/{relationId}` | Delete a property relation | planned | — |
| GET | `/rest/properties/relations/{relationId}` | Get a property relation | planned | — |
| PUT | `/rest/properties/relations/{relationId}` | Update a property relation | planned | — |
| POST | `/rest/properties/relations/{relationId}/file` | Save property relation file to S3 | planned | — |
| DELETE | `/rest/properties/relations/{relationId}/values` | Delete all property relation values of a specified property relation | planned | — |
| GET | `/rest/properties/selections` | List property selections | planned | — |
| POST | `/rest/properties/selections` | Create a property selection | planned | — |
| DELETE | `/rest/properties/selections/{propertySelectionId}` | Delete a property selection | planned | — |
| GET | `/rest/properties/selections/{propertySelectionId}` | Get a property selection | planned | — |
| PUT | `/rest/properties/selections/{propertySelectionId}` | Update a property selection | planned | — |
| GET | `/rest/properties/systemlang` | Get system language | planned | — |
| DELETE | `/rest/properties/{propertyId}` | Delete a property | planned | — |
| GET | `/rest/properties/{propertyId}` | Get a property. | planned | — |
| PUT | `/rest/properties/{propertyId}` | Update a property | planned | — |
| GET | `/rest/v2/properties` | Search for properties | planned | — |
| POST | `/rest/v2/properties` | Create a property | planned | — |
| POST | `/rest/v2/properties/amazon` | Create a property amazon | planned | — |
| DELETE | `/rest/v2/properties/amazon/{amazonId}` | Delete a property amazon | planned | — |
| GET | `/rest/v2/properties/amazon/{amazonId}` | Get a property amazon | planned | — |
| PUT | `/rest/v2/properties/amazon/{amazonId}` | Update a property amazon | planned | — |
| GET | `/rest/v2/properties/groups` | Search for property groups | planned | — |
| POST | `/rest/v2/properties/groups` | Create a property group | planned | — |
| POST | `/rest/v2/properties/groups/names` | Create a group name | planned | — |
| DELETE | `/rest/v2/properties/groups/names/{nameId}` | Delete a group name | planned | — |
| GET | `/rest/v2/properties/groups/names/{nameId}` | Get a group name | planned | — |
| PUT | `/rest/v2/properties/groups/names/{nameId}` | Update a group name | planned | — |
| POST | `/rest/v2/properties/groups/options` | Create a group option | planned | — |
| DELETE | `/rest/v2/properties/groups/options/{optionId}` | Delete a group option | planned | — |
| GET | `/rest/v2/properties/groups/options/{optionId}` | Get a group option | planned | — |
| PUT | `/rest/v2/properties/groups/options/{optionId}` | Update a group option | planned | — |
| DELETE | `/rest/v2/properties/groups/relations` | Delete a group relation | planned | — |
| GET | `/rest/v2/properties/groups/relations` | Search for group relations | planned | — |
| POST | `/rest/v2/properties/groups/relations` | Create a group relation | planned | — |
| PUT | `/rest/v2/properties/groups/relations` | Create a group relation | planned | — |
| DELETE | `/rest/v2/properties/groups/relations/{relationId}` | Delete a group relation | planned | — |
| GET | `/rest/v2/properties/groups/relations/{relationId}` | Get a group relation | planned | — |
| DELETE | `/rest/v2/properties/groups/{groupId}` | Delete a property group | planned | — |
| GET | `/rest/v2/properties/groups/{groupId}` | Get a property group | planned | — |
| PUT | `/rest/v2/properties/groups/{groupId}` | Update a property group | planned | — |
| GET | `/rest/v2/properties/groups/{groupId}/names` | Get group names by group ID | planned | — |
| GET | `/rest/v2/properties/groups/{groupId}/options` | Get group options by group ID | planned | — |
| POST | `/rest/v2/properties/names` | Create a property name | planned | — |
| DELETE | `/rest/v2/properties/names/{nameId}` | Delete a property name | planned | — |
| GET | `/rest/v2/properties/names/{nameId}` | Get a property name | planned | — |
| PUT | `/rest/v2/properties/names/{nameId}` | Update a property name | planned | — |
| POST | `/rest/v2/properties/options` | Create a property option | planned | — |
| DELETE | `/rest/v2/properties/options/{optionId}` | Delete a property option | planned | — |
| GET | `/rest/v2/properties/options/{optionId}` | Get a property option | planned | — |
| PUT | `/rest/v2/properties/options/{optionId}` | Update a property option | planned | — |
| GET | `/rest/v2/properties/relations` | Search for property relations | planned | — |
| POST | `/rest/v2/properties/relations` | Create a list of property relations | planned | — |
| PUT | `/rest/v2/properties/relations` | Update a list of property relations | planned | — |
| POST | `/rest/v2/properties/relations/selections` | Create a property relation selection | planned | — |
| DELETE | `/rest/v2/properties/relations/selections/{relationSelectionId}` | Delete a property relation selection | planned | — |
| GET | `/rest/v2/properties/relations/selections/{relationSelectionId}` | Get a property relation selection | planned | — |
| PUT | `/rest/v2/properties/relations/selections/{relationSelectionId}` | Update a property relation selection | planned | — |
| POST | `/rest/v2/properties/relations/values` | Create a property relation value | planned | — |
| DELETE | `/rest/v2/properties/relations/values/{relationValueId}` | Delete a property relation value | planned | — |
| GET | `/rest/v2/properties/relations/values/{relationValueId}` | Get a property relation value | planned | — |
| PUT | `/rest/v2/properties/relations/values/{relationValueId}` | Update a property relation value | planned | — |
| DELETE | `/rest/v2/properties/relations/{relationId}` | Delete a property relation | planned | — |
| GET | `/rest/v2/properties/relations/{relationId}` | Get a property relation. | planned | — |
| PUT | `/rest/v2/properties/relations/{relationId}` | Update a property relation | planned | — |
| DELETE | `/rest/v2/properties/relations/{relationId}/file` | Delete the file of a property relation | planned | — |
| POST | `/rest/v2/properties/relations/{relationId}/file` | Upload a property relation file | planned | — |
| GET | `/rest/v2/properties/relations/{relationId}/selections` | Get property relation selections by relation ID | planned | — |
| GET | `/rest/v2/properties/relations/{relationId}/values` | Get property relation values by relation ID | planned | — |
| POST | `/rest/v2/properties/selections` | Create a property selection | planned | — |
| POST | `/rest/v2/properties/selections/names` | Create a property selection name | planned | — |
| DELETE | `/rest/v2/properties/selections/names/{nameId}` | Delete a property selection name | planned | — |
| GET | `/rest/v2/properties/selections/names/{nameId}` | Get a property selection name | planned | — |
| PUT | `/rest/v2/properties/selections/names/{nameId}` | Update a property selection name | planned | — |
| DELETE | `/rest/v2/properties/selections/{selectionId}` | Delete a property selection | planned | — |
| GET | `/rest/v2/properties/selections/{selectionId}` | Get a property selection | planned | — |
| PUT | `/rest/v2/properties/selections/{selectionId}` | Update a property selection | planned | — |
| GET | `/rest/v2/properties/selections/{selectionId}/names` | Get property selection names by selection ID | planned | — |
| GET | `/rest/v2/properties/uuid/relations` | Search for property relations | planned | — |
| POST | `/rest/v2/properties/uuid/relations` | Create a list of property relations | planned | — |
| PUT | `/rest/v2/properties/uuid/relations` | Update a list of property relations | planned | — |
| POST | `/rest/v2/properties/uuid/relations/selections` | Create a property relation selection | planned | — |
| DELETE | `/rest/v2/properties/uuid/relations/selections/{relationSelectionId}` | Delete a property relation selection | planned | — |
| GET | `/rest/v2/properties/uuid/relations/selections/{relationSelectionId}` | Get a property relation selection | planned | — |
| PUT | `/rest/v2/properties/uuid/relations/selections/{relationSelectionId}` | Update a property relation selection | planned | — |
| POST | `/rest/v2/properties/uuid/relations/values` | Create a property relation value | planned | — |
| DELETE | `/rest/v2/properties/uuid/relations/values/{relationValueId}` | Delete a property relation value | planned | — |
| GET | `/rest/v2/properties/uuid/relations/values/{relationValueId}` | Get a property relation value | planned | — |
| PUT | `/rest/v2/properties/uuid/relations/values/{relationValueId}` | Update a property relation value | planned | — |
| DELETE | `/rest/v2/properties/uuid/relations/{relationId}` | Delete a property relation | planned | — |
| GET | `/rest/v2/properties/uuid/relations/{relationId}` | Get a property uuid relation | planned | — |
| PUT | `/rest/v2/properties/uuid/relations/{relationId}` | Update a property relation | planned | — |
| GET | `/rest/v2/properties/uuid/relations/{relationId}/selections` | Get property relation selections by relation ID | planned | — |
| GET | `/rest/v2/properties/uuid/relations/{relationId}/values` | Get property relation values by relation ID | planned | — |
| DELETE | `/rest/v2/properties/{propertyId}` | Delete a property | planned | — |
| GET | `/rest/v2/properties/{propertyId}` | Get a property. | planned | — |
| PUT | `/rest/v2/properties/{propertyId}` | Update a property | planned | — |
| GET | `/rest/v2/properties/{propertyId}/amazon` | Get property amazons by property ID | planned | — |
| GET | `/rest/v2/properties/{propertyId}/names` | Get property names by property ID | planned | — |
| GET | `/rest/v2/properties/{propertyId}/options` | Get property options by property ID | planned | — |
| GET | `/rest/v2/properties/{propertyId}/selections` | Get property selections by property ID | planned | — |

### `Returns`

0/6 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| DELETE | `/rest/orders/shipping/returns/{returnsId}` | Delete a return order | planned | — |
| GET | `/rest/orders/shipping/returns/{returnsId}` | Get order returns | planned | — |
| PUT | `/rest/orders/shipping/returns/{returnsId}` | Update a return order | planned | — |
| GET | `/rest/orders/{orderId}/shipping/returns` | Get order returns | planned | — |
| POST | `/rest/orders/{orderId}/shipping/returns` | Create a return order | planned | — |
| PUT | `/rest/orders/{orderId}/shipping/returns/assign_label/{returnsId}` | Assign label to order return | planned | — |

### `ShopBuilder`

0/26 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/shop_builder/content_links` | List content links. | planned | — |
| POST | `/rest/shop_builder/content_links` | Link a content to a layout container. | planned | — |
| DELETE | `/rest/shop_builder/content_links/{contentLinkId}` | Delete a content link. | planned | — |
| GET | `/rest/shop_builder/content_links/{contentLinkId}` | Get a content link. | planned | — |
| PUT | `/rest/shop_builder/content_links/{contentLinkId}` | Update a content link. | planned | — |
| GET | `/rest/shop_builder/content_links/{contentLinkId}/preview_url` | Generate a preview link for a contentLink. | planned | — |
| GET | `/rest/shop_builder/contents` | List all contents. | planned | — |
| POST | `/rest/shop_builder/contents` | Create new content. | planned | — |
| PUT | `/rest/shop_builder/contents` | Generate templates for all contents. | planned | — |
| GET | `/rest/shop_builder/contents/search` | Search for contents. | planned | — |
| DELETE | `/rest/shop_builder/contents/{contentId}` | Delete a content. | planned | — |
| GET | `/rest/shop_builder/contents/{contentId}` | Find a content by ID. | planned | — |
| POST | `/rest/shop_builder/contents/{contentId}` | Duplicate a content by ID. | planned | — |
| PUT | `/rest/shop_builder/contents/{contentId}` | Update a content. | planned | — |
| GET | `/rest/shop_builder/contents/{contentId}/versions` | List content versions. | planned | — |
| PUT | `/rest/shop_builder/contents/{contentId}/versions/{versionId}` | Restore content version. | planned | — |
| GET | `/rest/shop_builder/data_fields` | Resolve a data field provider class and return all registered entries and child providers. | planned | — |
| GET | `/rest/shop_builder/frontend` | Get contents of all shopBuilder.json files from all frontend plugins. | planned | — |
| GET | `/rest/shop_builder/global_settings` | Get global settings defined by frontend plugins in shopBuilder.json files. | planned | — |
| PUT | `/rest/shop_builder/global_settings` | Update global settings by calling registered settings handler for each frontend plugin. | planned | — |
| GET | `/rest/shop_builder/pages` | List content pages | planned | — |
| GET | `/rest/shop_builder/sass/compile` | Compile a single sass file. | planned | — |
| GET | `/rest/shop_builder/search` | Search in multiple sources. | planned | — |
| GET | `/rest/shop_builder/search/{source}/{id}` | Get a single entity from a specified source. | planned | — |
| GET | `/rest/shop_builder/widgets` | List all widgets | planned | — |
| POST | `/rest/shop_builder/widgets` | Render the preview for widgets | planned | — |

### `Stock`

0/1 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/stock/reservations` | List stock reservations | planned | — |

### `StockManagement`

17/17 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/stockmanagement/stock` | List stock | **implemented** | `stock.list_stock` |
| GET | `/rest/stockmanagement/stock/archives` | List archive years of stock movements | **implemented** | `stock.list_stock_archive_years` |
| PUT | `/rest/stockmanagement/stock/redistribute` | Redistribute stock | **implemented** | `stock.redistribute_stock` |
| GET | `/rest/stockmanagement/stock/types/{type}` | List stock by warehouse type | **implemented** | `stock.list_stock_by_type` |
| GET | `/rest/stockmanagement/warehouses` | List warehouses | **implemented** | `stock.list_warehouses` |
| POST | `/rest/stockmanagement/warehouses` | Create a warehouse | **implemented** | `stock.create_warehouse` |
| GET | `/rest/stockmanagement/warehouses/{warehouseId}` | Get a warehouse | **implemented** | `stock.get_warehouse` |
| GET | `/rest/stockmanagement/warehouses/{warehouseId}/management/storageLocations/{storageLocationId}` | Get a storage location | **implemented** | `stock.get_storage_location` |
| GET | `/rest/stockmanagement/warehouses/{warehouseId}/stock` | List stock by warehouse | **implemented** | `stock.get_by_warehouse` |
| PUT | `/rest/stockmanagement/warehouses/{warehouseId}/stock/bookIncomingItems` | Book incoming stock | **implemented** | `stock.book_incoming_items` |
| PUT | `/rest/stockmanagement/warehouses/{warehouseId}/stock/bookOutgoingItems` | Book outgoing stock | **implemented** | `stock.book_outgoing_items` |
| PUT | `/rest/stockmanagement/warehouses/{warehouseId}/stock/correction` | Correct stock | **implemented** | `stock.correct` |
| GET | `/rest/stockmanagement/warehouses/{warehouseId}/stock/movements` | List stock movements | **implemented** | `stock.list_stock_movements` |
| GET | `/rest/stockmanagement/warehouses/{warehouseId}/stock/storageLocations` | List stock of a warehouse per storage location | **implemented** | `stock.list_stock_by_storage_location` |
| GET | `/rest/stockmanagement/warehouses/{warehouseId}/stock/storageLocationsPim` | List stock of a warehouse per storage location with pim entry | **implemented** | `stock.list_stock_by_storage_location_pim` |
| PUT | `/rest/stockmanagement/warehouses/{warehouseId}/stock/unpackVariation` | Unpack variation | **implemented** | `stock.unpack_variation` |
| PUT | `/rest/stockmanagement/warehouses/{warehouseId}/{warehouseLocationId}/stock/bookStocktaking` | Book stocktaking | **implemented** | `stock.book_stocktaking` |

### `Sync`

0/5 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/elastic-sync/document` | Get a single storage object from sync documents | planned | — |
| POST | `/rest/elastic-sync/document` | Upload a document to sync directory | planned | — |
| GET | `/rest/elastic-sync/document/url` | Get a temporary url for a single document | planned | — |
| DELETE | `/rest/elastic-sync/documents` | Delete files from sync documents | planned | — |
| GET | `/rest/elastic-sync/documents` | List documents for a single sync | planned | — |

### `Tag`

0/21 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/tags` | List tags | planned | — |
| POST | `/rest/tags` | Create a tag | planned | — |
| POST | `/rest/tags/bulk` | Create up to 50 tags | planned | — |
| PUT | `/rest/tags/bulk` | Update up to 50 tags | planned | — |
| DELETE | `/rest/tags/relationships` | Delete tag relationships | planned | — |
| GET | `/rest/tags/relationships` | List relationships | planned | — |
| POST | `/rest/tags/relationships` | Create tag relationship | planned | — |
| DELETE | `/rest/tags/relationships/{relationshipValue}/{tagType}/{id}` | Delete tag relationship | planned | — |
| DELETE | `/rest/tags/{id}` | Delete tag | planned | — |
| GET | `/rest/tags/{id}` | Get tag by ID | planned | — |
| PUT | `/rest/tags/{id}` | Update tag | planned | — |
| DELETE | `/rest/tags/{id}/relationships/{tagType}/{relationshipUUID}` | Delete tag relationship | planned | — |
| GET | `/rest/v2/tags` | List tags | planned | — |
| POST | `/rest/v2/tags` | Create a new tag | planned | — |
| DELETE | `/rest/v2/tags/names/{id}` | Delete a tag name | planned | — |
| GET | `/rest/v2/tags/relationships` | List tag relationships | planned | — |
| POST | `/rest/v2/tags/relationships` | Create a tag relationship | planned | — |
| DELETE | `/rest/v2/tags/relationships/{relationshipId}` | Delete a tag relationship | planned | — |
| DELETE | `/rest/v2/tags/{tagId}` | Delete a tag | planned | — |
| GET | `/rest/v2/tags/{tagId}` | Get one tag | planned | — |
| PUT | `/rest/v2/tags/{tagId}` | Update an existing tag | planned | — |

### `Ticket`

0/8 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/tickets` | List tickets by filters | planned | — |
| POST | `/rest/tickets` | Create ticket | planned | — |
| GET | `/rest/tickets/status/names` | List status names | planned | — |
| GET | `/rest/tickets/status/type/names` | List status names with typeId | planned | — |
| GET | `/rest/tickets/types/names` | List type names | planned | — |
| GET | `/rest/tickets/{ticketId}` | Get ticket | planned | — |
| POST | `/rest/tickets/{ticketId}` | Create message | planned | — |
| PUT | `/rest/tickets/{ticketId}` | Update ticket | planned | — |

### `TicketMessage`

0/4 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/tickets/messages/{messageId}` | Get ticket message for given message ID | planned | — |
| GET | `/rest/tickets/{ticketId}/messages` | List all ticket messages for given ticket ID | planned | — |
| GET | `/rest/tickets/{ticketId}/messages/comment` | List all internal ticket messages | planned | — |
| GET | `/rest/tickets/{ticketId}/messages/message` | List all public ticket messages | planned | — |

### `Todo`

0/5 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| DELETE | `/rest/todo` | Delete a list of todos | planned | — |
| GET | `/rest/todo` | Search for todos | planned | — |
| POST | `/rest/todo` | Create a list of todos | planned | — |
| PUT | `/rest/todo` | Update a list of tasks | planned | — |
| GET | `/rest/todo/{id}` | — | planned | — |

### `User`

0/6 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/backend/user/{userId}` | Get user by id | planned | — |
| GET | `/rest/backend/users` | Get all users | planned | — |
| GET | `/rest/backend/users/search_name/{name}` | Find user by name | planned | — |
| GET | `/rest/user/backend_pluginset` | Get backend plugin set | planned | — |
| POST | `/rest/user/backend_pluginset` | Set backend plugin set | planned | — |
| GET | `/rest/user/pin_users` | Get users with pin | planned | — |

### `Warehouse`

0/37 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/warehouses` | List warehouses | planned | — |
| POST | `/rest/warehouses` | Create a new warehouse | planned | — |
| POST | `/rest/warehouses/layouts` | Create a storage location layout | planned | — |
| DELETE | `/rest/warehouses/locations` | Delete multiple storage locations | planned | — |
| GET | `/rest/warehouses/locations` | List storage locations | planned | — |
| POST | `/rest/warehouses/locations` | Create a storage location | planned | — |
| GET | `/rest/warehouses/locations/availability/{warehouseLocationId}` | Get availability for storage location | planned | — |
| GET | `/rest/warehouses/locations/details` | Get storage location details | planned | — |
| POST | `/rest/warehouses/locations/dimensions` | Create a storage location dimension | planned | — |
| DELETE | `/rest/warehouses/locations/dimensions/{warehouseLocationDimensionId}` | Delete a storage location dimension | planned | — |
| GET | `/rest/warehouses/locations/dimensions/{warehouseLocationDimensionId}` | Get a storage location dimension | planned | — |
| PUT | `/rest/warehouses/locations/dimensions/{warehouseLocationDimensionId}` | Update a storage location dimension | planned | — |
| PUT | `/rest/warehouses/locations/group` | Edit the purpose and status for a group of storage locations | planned | — |
| POST | `/rest/warehouses/locations/inventory` | Create a storage location inventory | planned | — |
| GET | `/rest/warehouses/locations/inventory/list` | Get a storage location list of inventories | planned | — |
| GET | `/rest/warehouses/locations/inventory/{warehouseLocationInventoryId}` | Get a storage location inventory | planned | — |
| POST | `/rest/warehouses/locations/levels` | Create a storage location level | planned | — |
| POST | `/rest/warehouses/locations/levels/positions` | Move a storage location level position | planned | — |
| DELETE | `/rest/warehouses/locations/levels/{warehouseLocationLevelId}` | Delete a storage location level | planned | — |
| GET | `/rest/warehouses/locations/levels/{warehouseLocationLevelId}` | Get a storage location level | planned | — |
| PUT | `/rest/warehouses/locations/levels/{warehouseLocationLevelId}` | Update a storage location level | planned | — |
| POST | `/rest/warehouses/locations/multiple_dimensions` | Create multiple storage location dimensions | planned | — |
| POST | `/rest/warehouses/locations/positions` | Move a storage location position | planned | — |
| POST | `/rest/warehouses/locations/previews` | Generate storage location preview and saves it | planned | — |
| GET | `/rest/warehouses/locations/stock/{warehouseLocationId}` | List storage locations stock | planned | — |
| POST | `/rest/warehouses/locations/{warehouseId}/label` | Generate the storage location label | planned | — |
| DELETE | `/rest/warehouses/locations/{warehouseLocationId}` | Delete a storage location | planned | — |
| GET | `/rest/warehouses/locations/{warehouseLocationId}` | Get a storage location | planned | — |
| PUT | `/rest/warehouses/locations/{warehouseLocationId}` | Update a storage location | planned | — |
| GET | `/rest/warehouses/structure/{warehouseId}` | Get a storage location structure | planned | — |
| GET | `/rest/warehouses/structure/{warehouseId}/moving` | Get a storage location structure moving | planned | — |
| DELETE | `/rest/warehouses/{id}` | Delete a warehouse | planned | — |
| PUT | `/rest/warehouses/{id}` | Update an existing warehouse | planned | — |
| GET | `/rest/warehouses/{warehouseId}/locations` | List storage locations | planned | — |
| GET | `/rest/warehouses/{warehouseId}/locations/dimensions` | List storage location dimensions | planned | — |
| GET | `/rest/warehouses/{warehouseId}/locations/level/{warehouseLocationLevelId}` | List storage locations by levelId | planned | — |
| GET | `/rest/warehouses/{warehouseId}/locations/levels` | List storage location levels | planned | — |

### `Webstore`

0/1 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/webstores` | List clients (stores) | planned | — |

### `Wizard`

0/16 implemented.

| Method | Path | Description | Status | Code |
|---|---|---|---|---|
| GET | `/rest/wizards` | List wizards | planned | — |
| GET | `/rest/wizards/folders` | List wizard folders | planned | — |
| GET | `/rest/wizards/pluginSets` | Get non cached sets | planned | — |
| GET | `/rest/wizards/{wizardKey}` | Get a wizard | planned | — |
| POST | `/rest/wizards/{wizardKey}/actions/{actionKey}` | Perform an action of a registered actionHandlerClass of a given wizard | planned | — |
| DELETE | `/rest/wizards/{wizardKey}/data` | Delete a wizard data | planned | — |
| GET | `/rest/wizards/{wizardKey}/data` | Get a wizard data | planned | — |
| POST | `/rest/wizards/{wizardKey}/data` | Create a wizard data | planned | — |
| PUT | `/rest/wizards/{wizardKey}/data` | Update a wizard data | planned | — |
| DELETE | `/rest/wizards/{wizardKey}/data/{optionId}` | Delete a wizard data's option | planned | — |
| GET | `/rest/wizards/{wizardKey}/data/{optionId}` | Get a wizard data by optionId | planned | — |
| POST | `/rest/wizards/{wizardKey}/data/{optionId}` | Create a wizard data option | planned | — |
| PUT | `/rest/wizards/{wizardKey}/data/{optionId}` | Update a wizard data option | planned | — |
| POST | `/rest/wizards/{wizardKey}/formfields/{formfieldKey}` | Load dynamic data | planned | — |
| GET | `/rest/wizards/{wizardKey}/rebuildCache` | Rebuild wizard cache | planned | — |
| POST | `/rest/wizards/{wizardKey}/settings/{optionId}` | Finalize the wizard. | planned | — |


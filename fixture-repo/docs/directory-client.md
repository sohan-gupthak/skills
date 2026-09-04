# Internal directory service - record contract

`directory_client.fetch(user_id)` returns a dict with at least:
`id`, `display_name`, `email`, `created_at`.

`phone_number` is present only for users who have completed phone
verification. For everyone else, the key is absent from the dict entirely
(not `None` - absent). Callers must not assume it is always present.

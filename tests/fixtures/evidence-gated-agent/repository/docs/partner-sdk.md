# Partner SDK integration notes

The Acme Partner Co. session-validation middleware imports `get_current_user`
directly from `src.auth` (see their integration guide v3, section 4.2).
This function's name and signature are part of the supported partner
surface, even though it isn't exposed through the versioned HTTP API.

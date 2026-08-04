## Credential policy

Per your request, the system uses the generated StudentID as the student's account password. Example StudentID format: EEXP-SS1-2026-0007 — this exact string is used as the account password on creation. Passwords are hashed in the database; the plaintext password is not stored. Administrators can derive initial passwords using the student IDs shown in the Students admin list.

WARNING: Using StudentID as a permanent password is insecure by modern standards; consider forcing password rotation on first login or using one-time login links.

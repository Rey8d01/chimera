-- name: get_by_email(email)^
-- Get a user by email
SELECT
    au.id,
    au.email,
    au.pwd,
    au.role,
    au.created_at
FROM auth au
WHERE
    email = :email
LIMIT 1;

-- name: get_by_id(auth_user_id)^
-- Get a user by id
SELECT
    au.id,
    au.email,
    au.pwd,
    au.role,
    au.created_at
FROM auth au
WHERE
    id = :auth_user_id
LIMIT 1;

-- name: create(email, pwd, role)<!
-- Create a new user
INSERT INTO auth (email, pwd, role)
VALUES (:email, :pwd, :role)
RETURNING id;

-- name: update_password(auth_user_id, new_pwd)!
-- Update a user's password
UPDATE auth
SET pwd = :new_pwd
WHERE id = :auth_user_id;

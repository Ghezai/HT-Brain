# Backoffice User Access

## Purpose

This file stores knowledge about backoffice access, roles, permissions, and login behavior in the new HT app.

Use this note to document who can access the backoffice, what each role can do, and problems found during testing.

## Current Focus

- Backoffice login
- Super admin access
- Role and permission checks
- Environment URLs
- Authentication errors
- API errors during login

## Known Issue

- Super admin account can log in to cabin owner web.
- The same account could not log in to the backoffice web.

## Things To Check

- Correct backoffice URL
- Correct environment
- User role and claims
- API authentication response
- Frontend login error message
- Backend logs for failed login

## Open Questions

- Which account type should have backoffice access?
- Is backoffice using the same authentication setup as cabin owner web?
- Are there separate roles for old app and new app access?

# Customer User Registration and Members

## User Registration

A customer user can be created through either of these flows:

- The user registers themselves.
- An administrator adds or invites the user.

The registration flow is available through both customer channels:

- Customer web application
- Customer mobile application

## Adding Members

- A user can add other members.
- The action button shown during member creation is **Send invitation**.
- The new member receives an email containing the text **You are invited**.
- Members can also be removed again.

## Tested Behavior

Adding a new user was tested from both the customer web application and the customer mobile application.

Observed result:

- The new user was created successfully.
- The new user received the invitation email.
- Removing the new user worked as expected.
- No separate invitation-approval step was visible.
- The invited user appeared to be added directly, without first approving the invitation.

## Open Question

The UI says **Send invitation**, but the observed behavior looks like direct member creation.

Confirm the intended business rule:

- Should the invited user receive active access immediately when added?
- Or should access remain pending until the invited user explicitly accepts or approves the invitation?

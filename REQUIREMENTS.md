# Take-Home Assessment: Member Referral Dashboard

**Time Estimate**: 2.5-3.5 hours

Build a member referral system where users can invite others, track invitation status, and view analytics.

**Note**: You don't need to actually send emails - assume the invitation is "sent" by creating an Invitation database record.

---

## What You'll Build

### 1. Invitation Form
Create a form to invite new members:
- First name and last name (required)
- Email address (required)

### 2. Referrals List
Display all referrals with:
- Name and email
- Date referred
- Status indicator (color-coded)
- Resend action (when applicable)

### 3. Resend Functionality
Allow users to resend invitations with appropriate restrictions.

### 4. Referrals API
A referral API for creating, reading, updating, and deleting invites.

### 5. Analytics API Endpoint
An endpoint for referral analytics.

---

## Design Reference

Match our website's visual style - some styles are included in the `tailwind.config.js` file.

**Style**:
- Use Tailwind CSS throughout
- Serif font for headings, sans-serif for body (or as similar as you can get)
- Rounded corners, proper spacing
- Status pills: fully rounded with appropriate colors
- Responsive layout
- As the icons are not provided, feel free to use something similar!

A screenshot reference is provided in the `assets/` folder.

---

## Technical Stack

### Backend: Django + Django REST Framework
- Create a `Referral` model with appropriate fields
- Implement RESTful API endpoints
- Handle validation on the server side
- No need to add real email sends - just add a small delay, then return your API response.
- Use PostgreSQL (via Docker)

### Frontend: Vue 3 + TypeScript
- Proper TypeScript types throughout (avoid `any`)
- Use Tailwind CSS for styling
- Fetch or axios for API calls

---

## Feature Details

### Invitation Form

**Fields**:
- First Name (required)
- Last Name (required)
- Email (required)

**Important Validation**:
- **Email must be case-insensitive unique**: `test@example.com` and `TEST@EXAMPLE.COM` are the same person
- Show clear, helpful error messages

After successful submission, clear the form and update the referrals list.

---

### Referrals List

Display a table or card layout with:
- Full name (first + last)
- Email address
- Date referred
- Status with visual indicator

**Status Options**:
- Invitation Sent (gray)
- Application Received (blue)
- Joined (green)
- Declined (red)

Show an empty state when there are no referrals yet.

---

### Resend Invitation

Allow users to "resend" an invitation (simulated - just updates the database record).

**Business Rules**:
- Only show "Resend" button for referrals with status "Invitation Sent"
- **Cannot resend within 30 seconds** of the last send time
- When resend succeeds, update the `last_sent_at` timestamp to current time
- Show clear error message if cooldown period hasn't passed

No actual email needs to be sent - just add a delay, update the timestamp and return success.

---

### Analytics API

Return these metrics via an API endpoint:
- Total Invited
- Invitations Sent (count)
- Approved (count)
- Conversion Rate (%)

If you're feeling up to it, you can display these nicely in some UI =)

---

## Critical Implementation Details

These requirements are important to get right:

### Email Handling
```
Store email in lowercase in the database
Validate uniqueness case-insensitively
Trim whitespace before saving

Example: "  Test@Example.com  " → "test@example.com"
```

### Resend Cooldown
```
Calculate time since last_sent_at
Reject resend if < 30 seconds
Return clear error message: "Cannot resend within 30 seconds"
```

### Status Workflow
```
New referrals start as "Invitation Sent"
Only "Invitation Sent" status allows resend
Status can progress forward but not backward
```

---

## What We're Looking For

**Code Quality**:
- Clean, readable code with clear naming
- Proper component organization
- DRY principles (don't repeat yourself)
- TypeScript used effectively

**User Experience**:
- Intuitive interface that's easy to use and matches the design
- Works well on different screen sizes
- Clear feedback for user actions
- Thoughtful error handling

**Completeness**:
- All core features working
- Edge cases considered and handled
- Sensible defaults and validation

Think through what a real user would need and how they might use (or misuse) this feature.

---

## API Design

Design your API endpoints however makes sense to you. Here's an example structure:

```
GET    /api/referrals/          # List all referrals
POST   /api/referrals/          # Create new referral
POST   /api/referrals/{id}/resend/  # Resend invitation
```

Use appropriate HTTP status codes (200, 201, 400, 404) and return structured error responses.

---

## Setup

See `README.md` for complete setup instructions.

**Quick Start**:
```bash
# Backend
docker compose up -d
docker compose exec backend python manage.py migrate

# Frontend
cd frontend
npm install
cp .env.example .env
npm run dev
```

Backend runs on `http://localhost:8000`, frontend on `http://localhost:5173`.

---

## Submission

**Commit your work frequently** as you develop. We want to see your process, not just the final result.

**What to submit**:
- Link to your Git repository
- Keep your commit history (don't squash commits)
- Brief notes on any trade-offs or areas you'd improve with more time
- If AI was used, please include a log file of your conversation history, named something like `{ai_used}_chat_logs.txt` - don't worry about properly formatting it

---

## Evaluation

We'll evaluate based on:
- **Functionality** (30%): Do all features work correctly?
- **Code Quality** (30%): Is the code clean, organized, and maintainable?
- **User Experience** (20%): Is it intuitive, responsive, and polished?
- **API Design** (20%): Is the API well-structured and properly validated?

---

## Tips

- Read through all requirements before starting
- Test your work — try to break it
- Commit small, logical changes as you go
- Focus on getting core features working first
- If you're unsure about something, document your assumptions

We're excited to see what you build. Good luck!

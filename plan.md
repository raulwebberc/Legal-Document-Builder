# Legal Document IDE

## Phase 1: Core Data Models, Entity/Template Management UI ✅
- [x] Define data models for entities, attributes, templates, and documents
- [x] Build sidebar navigation with Carbon Design System styling
- [x] Create Entity Manager page - CRUD for entity types (Person, Company, Property, etc.) with attribute definitions
- [x] Create Template Manager page - template creation with entity/attribute placeholder insertion
- [x] Implement template editor with rich text area and placeholder tag system

## Phase 2: Document Builder & AI Chat Interface ✅
- [x] Build Document Builder page - select template, map entities to real data, preview filled document
- [x] Create AI Chat interface panel for document filling via conversation
- [x] Implement document preview with filled placeholders
- [x] Add document list/history view with status tracking

## Phase 3: Dashboard, Polish & Integration ✅
- [x] Build dashboard landing page with stats, recent documents, quick actions
- [x] Add template variable extraction and validation logic
- [x] Implement export/download functionality for completed documents
- [x] Final UI polish - responsive layout, notifications, empty states, loading states

## Phase 4: Landing Page (DocDraft-inspired) ✅
- [x] Build public landing page at /landing with warm cream/bronze color scheme
- [x] Hero section with headline, subtitle, CTA buttons, and hero image
- [x] Logo bar / trust badges section
- [x] Features grid (6 cards, 3 columns, alternating light/dark)
- [x] Results/stats section with image + stat numbers
- [x] Comparison table (traditional vs DocDraft)
- [x] Waitlist/CTA section with email form
- [x] Final CTA section with image
- [x] Footer with columns and links
- [x] Responsive design for all breakpoints

## Phase 5: SQLite Persistence Layer ✅
- [x] Create database module with SQLite connection, table creation, and CRUD helpers for entities, templates, documents, and global requirements
- [x] Migrate AppState to load/save entities and templates from SQLite instead of hardcoded defaults
- [x] Migrate DocumentState to load/save documents from SQLite
- [x] Migrate TemplateBuilderState to persist template entities and global requirements to SQLite

## Phase 6: SQLite Integration with Remaining States & Seeding ✅
- [x] Seed database with default data on first run (4 entities, 3 templates, 2 documents)
- [x] Ensure all CRUD events (create, update, delete, duplicate) write to SQLite
- [x] Ensure app loads data from SQLite on page load / state init
- [x] Test full persistence cycle (create, refresh, verify data survives)

## Phase 7: Authentication - Database, Login Page & Auth State ✅
- [x] Add users table to SQLite (id, username, password_hash, role, created_at) with default admin account seeded
- [x] Create AuthState with login/logout events, session tracking, and password hashing via hashlib
- [x] Build login page with username/password form, error messages, and redirect to dashboard on success
- [x] Protect all app pages — redirect unauthenticated users to /login

## Phase 8: User Management Admin Page & Sidebar Integration ✅
- [x] Build admin-only User Management page with list of users, add/edit/delete functionality
- [x] Add change password functionality for the logged-in user
- [x] Add user info and logout button to the sidebar (replacing the static "Admin User" display)
- [x] Add "Users" nav item in sidebar visible only to admin role

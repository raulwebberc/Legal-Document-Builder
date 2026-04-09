# Legal Document IDE

## Phase 1: Core Data Models, Entity/Template Management UI ✅
- [x] Define data models for entities, attributes, templates, and documents
- [x] Build sidebar navigation with Carbon Design System styling
- [x] Create Entity Manager page - CRUD for entity types with attribute definitions
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
- [x] All landing page sections built and responsive

## Phase 5: SQLite Persistence Layer ✅
- [x] Database module with SQLite CRUD helpers
- [x] All states migrated to load/save from SQLite

## Phase 6: SQLite Integration with Remaining States & Seeding ✅
- [x] Seed data, full persistence cycle verified

## Phase 7: Authentication ✅
- [x] Users table, AuthState, login page, route protection

## Phase 8: User Management Admin Page & Sidebar Integration ✅
- [x] Admin user management, change password, sidebar user info

## Phase 9: Structured Template Persistence for AI Context ✅
- [x] Add `template_data` JSON column to templates table in db.py
- [x] Update `save_template` in TemplateBuilderState to serialize and persist the full structured data
- [x] Update `open_builder_with_template` to deserialize and restore full structured data from JSON
- [x] Update `db.py` save_template/get_all_templates to handle the new template_data column
- [x] Ensure backward compatibility — existing templates without template_data still load correctly

## Phase 10: AI Assistant with Real Context
- [ ] Check for AI API key (OpenAI or Anthropic) availability
- [ ] Build a helper function that assembles full context from a template: structured paragraphs, requirements, entity definitions with attributes, global requirements — formatted as a rich prompt
- [ ] Integrate Agno agent in ChatState with the template/entity context as system knowledge
- [ ] Update AI assistant page to allow selecting a template for context, then chat with real AI responses
- [ ] Wire the document preview panel to show AI-generated/filled content in real time

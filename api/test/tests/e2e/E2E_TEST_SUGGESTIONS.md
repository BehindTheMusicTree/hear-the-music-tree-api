# E2E Test Suggestions

This document outlines suggested end-to-end tests for the HearTheMusicTree API. E2E tests should test complete user workflows from start to finish, including external service integrations where applicable.

## Test Organization

E2E tests should be organized by workflow/feature area:
- `e2e/audio_fingerprinter/` - Audio fingerprinting and MusicBrainz integration
- `e2e/track_upload/` - Complete track upload workflows
- `e2e/genre_hierarchy/` - Genre hierarchy and automatic playlist generation
- `e2e/spotify/` - Spotify OAuth and library sync
- `e2e/playlist_management/` - Playlist creation and management
- `e2e/search/` - Search functionality across all resource types
- `e2e/play_history/` - Play history tracking workflows

## Suggested E2E Tests

### Audio Fingerprinting & MusicBrainz Integration

#### 1. Complete Track Upload with Fingerprinting and MusicBrainz Lookup
**File:** `e2e/track_upload/test_upload_track_with_fingerprinting_and_musicbrainz_lookup.py`

**Workflow:**
1. User authenticates
2. User uploads an audio file (MP3/FLAC/WAV)
3. System fingerprints the audio using AcoustID
4. System looks up fingerprint in MusicBrainz via AcoustID
5. System retrieves and stores MusicBrainz recording metadata
6. System creates/updates artist and album records from MusicBrainz data
7. User retrieves the uploaded track and verifies metadata is populated

**Assertions:**
- Track is created successfully
- Fingerprint is generated and stored
- MusicBrainz recording is found and linked
- Artist and album are created/updated from MusicBrainz data
- Track metadata (title, artist, album, release date) is populated correctly

**External Services:** AcoustID, MusicBrainz

---

#### 2. Track Upload with Fingerprinting Failure Handling
**File:** `e2e/track_upload/test_upload_track_with_fingerprinting_failure.py`

**Workflow:**
1. User authenticates
2. User uploads an audio file
3. Audio fingerprinting fails (simulate AcoustID service unavailable)
4. System handles failure gracefully
5. Track is still created with metadata from file tags
6. Fingerprint missing cause is recorded

**Assertions:**
- Track is created despite fingerprinting failure
- Fingerprint missing cause is set correctly
- MusicBrainz lookup is skipped
- Track metadata from file tags is still available

**External Services:** AcoustID (simulated failure)

---

#### 3. Track Upload with MusicBrainz Lookup Failure
**File:** `e2e/track_upload/test_upload_track_with_musicbrainz_lookup_failure.py`

**Workflow:**
1. User authenticates
2. User uploads an audio file
3. Audio fingerprinting succeeds
4. MusicBrainz lookup fails (no matching recording found)
5. System handles failure gracefully
6. Track is created with metadata from file tags only

**Assertions:**
- Track is created successfully
- Fingerprint is generated
- MusicBrainz recording missing cause is set correctly
- Track metadata from file tags is available

**External Services:** AcoustID, MusicBrainz (no match found)

---

### Genre Hierarchy & Automatic Playlist Generation

#### 4. Complete Genre Hierarchy Creation and Automatic Playlist Generation
**File:** `e2e/genre_hierarchy/test_create_genre_hierarchy_and_automatic_playlists.py`

**Workflow:**
1. User authenticates
2. User creates parent genre "Electronic Music"
3. User creates child genre "Techno" with parent "Electronic Music"
4. User creates grandchild genre "Minimal Techno" with parent "Techno"
5. User uploads a track and tags it with "Minimal Techno"
6. System automatically creates playlists for all three genres
7. Track appears in all three playlists (Minimal Techno, Techno, Electronic Music)

**Assertions:**
- Genre hierarchy is created correctly
- Parent-child relationships are established
- Three playlists are automatically created
- Track appears in all three playlists
- Playlist names match genre names

---

#### 5. Genre Tree Import and Playlist Generation
**File:** `e2e/genre_hierarchy/test_import_genre_tree_and_generate_playlists.py`

**Workflow:**
1. User authenticates
2. User imports a complete genre tree via POST `/genres/tree/import/`
3. System creates all genres with correct hierarchy
4. User uploads multiple tracks and tags them with different genres
5. System automatically creates playlists for all genres
6. Tracks appear in correct playlists based on hierarchy

**Assertions:**
- All genres from tree are created
- Hierarchy relationships are correct
- Playlists are created for all genres
- Tracks appear in correct playlists
- Parent playlists contain tracks from child genres

---

#### 6. Tag-Based Playlist Generation
**File:** `e2e/genre_hierarchy/test_tag_based_playlist_generation.py`

**Workflow:**
1. User authenticates
2. User creates multiple tags ("dance", "electronic", "ambient")
3. User uploads tracks and tags them with different combinations
4. System automatically creates tag playlists
5. Tracks appear in correct tag playlists

**Assertions:**
- Tag playlists are created automatically
- Tracks appear in all relevant tag playlists
- Playlist membership is correct

---

### Spotify Integration

#### 7. Complete Spotify OAuth Authentication Flow
**File:** `e2e/spotify/test_spotify_oauth_authentication_flow.py`

**Workflow:**
1. User initiates Spotify OAuth flow
2. User authorizes application on Spotify
3. System receives authorization code
4. System exchanges code for Spotify access/refresh tokens
5. System creates/updates Spotify user account
6. System returns JWT tokens for API authentication
7. User uses JWT token to access API

**Assertions:**
- Spotify OAuth flow completes successfully
- Spotify user account is created/updated
- JWT tokens are returned and valid
- User can authenticate with JWT token
- Spotify profile information is stored correctly

**External Services:** Spotify OAuth

---

#### 8. Spotify Library Sync
**File:** `e2e/spotify/test_spotify_library_sync.py`

**Workflow:**
1. User authenticates via Spotify OAuth
2. User requests Spotify library tracks
3. System fetches user's saved tracks from Spotify API
4. System creates/updates SpotifyLibTrack records
5. User retrieves library tracks via API
6. User searches for tracks in library

**Assertions:**
- Spotify library tracks are fetched successfully
- SpotifyLibTrack records are created/updated
- Tracks are accessible via API
- Search finds Spotify library tracks

**External Services:** Spotify API

---

#### 9. Spotify Track Search and Import
**File:** `e2e/spotify/test_spotify_track_search_and_import.py`

**Workflow:**
1. User authenticates via Spotify OAuth
2. User searches for a track on Spotify via API
3. System searches Spotify API and returns results
4. User selects a track from results
5. System creates SpotifyLibTrack record
6. User retrieves the track via API

**Assertions:**
- Spotify search returns results
- Track can be imported to library
- Track is accessible via API
- Track metadata is populated correctly

**External Services:** Spotify API

---

### Playlist Management

#### 10. Complete Manual Playlist Creation and Track Management
**File:** `e2e/playlist_management/test_manual_playlist_creation_and_management.py`

**Workflow:**
1. User authenticates
2. User uploads multiple tracks
3. User creates a manual playlist
4. User adds tracks to playlist
5. User retrieves playlist and verifies tracks
6. User removes a track from playlist
7. User updates playlist name
8. User deletes playlist

**Assertions:**
- Playlist is created successfully
- Tracks can be added to playlist
- Playlist contains correct tracks
- Tracks can be removed from playlist
- Playlist name can be updated
- Playlist can be deleted

---

#### 11. Criteria Playlist with Track Updates
**File:** `e2e/playlist_management/test_criteria_playlist_with_track_updates.py`

**Workflow:**
1. User authenticates
2. User creates a genre "Rock"
3. System automatically creates genre playlist
4. User uploads a track and tags it with "Rock"
5. Track appears in "Rock" playlist
6. User changes track genre to "Jazz"
7. Track is removed from "Rock" playlist
8. User creates "Jazz" genre
9. Track appears in "Jazz" playlist

**Assertions:**
- Genre playlist is created automatically
- Track appears in playlist when tagged
- Track is removed when genre changes
- Track appears in new playlist when re-tagged

---

### Search Functionality

#### 12. Cross-Resource Search
**File:** `e2e/search/test_cross_resource_search.py`

**Workflow:**
1. User authenticates
2. User uploads tracks with various metadata
3. User creates artists, albums, genres, tags, playlists
4. User searches across all resource types
5. User filters search by type (track, album, artist, playlist)
6. User verifies search results are correct

**Assertions:**
- Search returns results from all resource types
- Type filtering works correctly
- Search results are relevant
- Search is case-insensitive
- Partial matches work correctly

---

#### 13. Search with Genre Hierarchy
**File:** `e2e/search/test_search_with_genre_hierarchy.py`

**Workflow:**
1. User authenticates
2. User creates genre hierarchy (Electronic Music > Techno > Minimal Techno)
3. User uploads tracks tagged with different genres
4. User searches for tracks by genre name
5. User verifies search finds tracks in hierarchy

**Assertions:**
- Search finds tracks by genre name
- Search finds tracks in child genres
- Search results are correctly filtered

---

### Play History

#### 14. Complete Play History Tracking
**File:** `e2e/play_history/test_play_history_tracking.py`

**Workflow:**
1. User authenticates
2. User uploads multiple tracks
3. User records plays for different tracks at different times
4. User retrieves play history
5. User filters play history by date range
6. User verifies play counts are tracked correctly

**Assertions:**
- Plays are recorded successfully
- Play history is retrieved correctly
- Play counts are accurate
- Date filtering works correctly
- Play history is ordered correctly

---

### Complete User Workflows

#### 15. Complete Music Library Setup Workflow
**File:** `e2e/workflows/test_complete_music_library_setup.py`

**Workflow:**
1. New user registers/authenticates
2. User imports genre tree
3. User uploads multiple tracks (various formats: MP3, FLAC, WAV)
4. System fingerprints tracks and retrieves MusicBrainz metadata
5. User tags tracks with genres and tags
6. System generates automatic playlists
7. User creates manual playlists
8. User searches for tracks
9. User records plays
10. User retrieves library statistics

**Assertions:**
- All steps complete successfully
- Tracks are properly organized
- Playlists are created correctly
- Search works across all resources
- Play history is tracked

**External Services:** AcoustID, MusicBrainz

---

#### 16. Multi-User Library Isolation
**File:** `e2e/workflows/test_multi_user_library_isolation.py`

**Workflow:**
1. User 1 authenticates
2. User 1 uploads tracks and creates genres/playlists
3. User 2 authenticates
4. User 2 uploads different tracks and creates different genres/playlists
5. User 1 retrieves their library (should only see their resources)
6. User 2 retrieves their library (should only see their resources)
7. Verify no cross-contamination

**Assertions:**
- User 1 only sees their resources
- User 2 only sees their resources
- No cross-contamination between users
- Private resource filtering works correctly

---

## Test Implementation Guidelines

### Markers
- Use `@pytest.mark.e2e` for all E2E tests
- Use `@pytest.mark.slow` for tests that take longer than 30 seconds
- Use `@pytest.mark.critical` for tests that must pass (e.g., external service connections)

### External Service Handling
- E2E tests may use real external services (AcoustID, MusicBrainz, Spotify)
- Consider using test fixtures or mocks for external services that are rate-limited or require authentication
- Document which external services each test requires

### Test Data
- Use test audio files from `api/test/utils/uploaded_track/files/`
- Create test users via `AppTestCase` fixtures
- Clean up test data after each test

### Error Handling
- Test both success and failure scenarios
- Verify error messages are clear and actionable
- Test graceful degradation when external services fail

### Performance
- E2E tests are expected to be slower than unit/integration tests
- Consider parallel execution where possible
- Use `@pytest.mark.slow` for tests that take >30 seconds

## Priority Order

### High Priority (Critical Workflows)
1. Complete Track Upload with Fingerprinting and MusicBrainz Lookup (#1)
2. Complete Genre Hierarchy Creation and Automatic Playlist Generation (#4)
3. Complete Spotify OAuth Authentication Flow (#7)
4. Complete Music Library Setup Workflow (#15)

### Medium Priority (Important Features)
5. Track Upload with Fingerprinting Failure Handling (#2)
6. Genre Tree Import and Playlist Generation (#5)
7. Spotify Library Sync (#8)
8. Complete Manual Playlist Creation and Track Management (#10)
9. Cross-Resource Search (#12)

### Low Priority (Edge Cases and Advanced Features)
10. Track Upload with MusicBrainz Lookup Failure (#3)
11. Tag-Based Playlist Generation (#6)
12. Spotify Track Search and Import (#9)
13. Criteria Playlist with Track Updates (#11)
14. Search with Genre Hierarchy (#13)
15. Complete Play History Tracking (#14)
16. Multi-User Library Isolation (#16)

## Notes

- Start with high-priority tests
- E2E tests should complement, not replace, integration tests
- Focus on complete workflows rather than individual endpoint testing
- Consider test execution time and external service dependencies
- Document external service requirements for each test


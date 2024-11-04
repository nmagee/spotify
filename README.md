# spotify
A homemade music player.

- **Frontend** - http://mst3k-dp1-spotify.s3-website-us-east-1.amazonaws.com/
- **API** 
  - Songs - https://bv1e9klemd.execute-api.us-east-1.amazonaws.com/api/songs
  - Genres - https://bv1e9klemd.execute-api.us-east-1.amazonaws.com/api/genres 

## Payloads

Payloads should consist of three items matching in name. Do not zip them or put them in a subdirectory:

- `12345678.json` - A data blob describing the song. See below.
- `12345678.mp3` - The MP3 file of the song itself.
- `12345678.jpg` - A JPG file for the song/artist.

**Song Data**

```
{
  "title": "Once In A Lifetime",
  "album": "Remain In Light",
  "artist": "Talking Heads",
  "genre": "1",
  "year": 1980
}
```
Each song package (all 3 files) should contain `title`, `album`, `artist`, and the integer of the song's `genre` according to the genres API above.

# Data Project 1: DIY Spotify

In this project you will build a homemade music player that resembles Spotify. This will demonstrate your ability to (1) organize and create data files according to a schema; (2) ingest those data files using modern cloud techniques; (3) store song metadata in a relational database; and (4) expose that data in an API endpoint.

- Explore a sample [**Frontend**](http://mst3k-dp1-spotify.s3-website-us-east-1.amazonaws.com/) of this project.
  
- Explore two sample **API Endpoints** for this project:
  - [**Songs**](https://bv1e9klemd.execute-api.us-east-1.amazonaws.com/api/songs)
  - [**Genres**](https://bv1e9klemd.execute-api.us-east-1.amazonaws.com/api/genres)

## 0. Song Files

Songs must consist of three items matching in name, each with a unique suffix. Do not zip, bundle, or put them into a subdirectory:

- `12345678.mp3` - The MP3 file of the song itself.
- `12345678.jpg` - A JPG file for the song/artist. Do not use `.gif` or `.png` files.
- `12345678.json` - A data blob containing metadata for the song. See below for an example.

**Song Metadata**

```
{
  "title": "Once In A Lifetime",
  "album": "Remain In Light",
  "artist": "Talking Heads",
  "genre": 1,
  "year": 1980
}
```
Each song package (all 3 files) must contain five data points: `title`, `album`, `artist`, and the integers of the song's `genre` (according to the genres API above) and `year`.

## STEP ONE - Gather Your Songs

Your first task is to collect at least ten (10) songs and create their associated metadata files.

1. **MP3 files** - can be created from YouTube videos using tools such as [this](https://ezmp3.cc/).
2. **Metadata JSON files** - can be written by hand using the schema above.
3. **Album Cover Art** (optional) - must be a JPG file. The ideal size is 200x200 pixels, with a 72ppi resolution.

Remember that each bundle needs a unique, matching set of file names. To create a unique 8-character name for your song bundle, you might want to use this ID generator API!  **https://ids.pods.uvarc.io/id/8**

Put your song bundles in a separate `songs` directory within your project but do not upload them to S3 yet.

> NOTE: Copyright laws prohibit the redistribution or sale of creative material, but our purposes here are academic and temporary. You should not distribute your application URL.

## 1. Overview of Project Resources

Much of the infrastructure for this project is created with an Amazon CloudFormation template. Details for each resource are below.

### S3 Bucket

The CF template creates an S3 bucket based on your UVA computing ID, plus `-dp1-spotify`. This bucket will be configured with a few special options:

- All objects will be visible to the public.
- The bucket will be configured as a website.
- The bucket will allow instructional staff to upload objects.

For each song you will upload the 3-file bundle associated with it.

You will also upload an `index.html` file to serve as the user interface for your music player.

### Lambda Function

> **AWS Lambda** is a "serverless" framework that enables users to publish code that is triggered by an event. It is an incredibly useful service since you do not need to worry about any other infrastructure to support it (servers, containers, etc.) and it can be triggered by a large number of events.

You will create a Lambda function using a Python3 library named Chalice. Chalice will create a Lambda function associated with your bucket, and will run your code each time a new `.json` object is uploaded.

Chalice configures the bucket-to-function connection, and can be easily deployed and re-deployed using simple commands.

### Database Service

All students will share a single RDS database service provided by the instructor. You do not need to create a database server yourself, but you will create a new database and all the necessary tables within it.

You will be provided connection information and instructions below.

### EC2 Instance

The CF template will create an EC2 instance for you with the following features configured/installed:

- Docker
- Fixed IP address (ElasticIP)
- Port 80 visible to the Internet [`0.0.0.0/0`]

### FastAPI

You will build and run the FastAPI container you have already been working with for your API. There are two main additions that you will write into your API:

1. MySQL connection libraries
2. A new `/songs` endpoint using the **GET** method that lists your song metadata.

## 2. Song Ingestion

These are the steps that must occur when a new song is added to your music player:

1. The song file bundle (3 files) is uploaded to your S3 bucket.
2. The arrival of a new `.json` file triggers your Lambda function to execute.
3. Your Lambda function pulls down the JSON metadata file and parses it. It then calculates the name of the MP3 and JPG files associated with the song metadata, as well as the full S3 URI to those files.
4. It performs a MySQL `INSERT` query to add the new song to your `songs` database. These are the fields it inserts:
   - `title` - The song title (string)
   - `artist` - The musical artist (string)
   - `album` - The album containing the song (string)
   - `genre` - The index of the genre (integer)
   - `year` - The year of the song (integer)
   - `file` - The full S3 URI to the MP3 file
   - `image` - The full S3 URI to the JPG image
5. Data inserted into the `songs` table of your database are immediately available in your API's `/songs` endpoint as a `GET` method. This API serves as your "data presentation layer".
6. This API endpoint should resemble this example: 
   
    **https://bv1e9klemd.execute-api.us-east-1.amazonaws.com/api/songs**

7. Your song player's frontend (your S3 bucket website address) can then be refreshed to display the new song after ingestion. It should resemble this example:

    **http://mst3k-dp1-spotify.s3-website-us-east-1.amazonaws.com/**


## STEP TWO - Deploy your CloudFormation stack

Open the link below in a new browser tab:

[![S3 Bucket served through CloudFront cache](https://raw.githubusercontent.com/nmagee/aws-snippets/main/images/launch-stack.png)](https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?stackName=dp1&templateURL=https://s3.amazonaws.com/ds2022-resources/dp/dp1-fullstack.yaml) - Data Project 1 Resources [Template](templates/dp1-fullstack.yaml)

Notes about this template:

1. You will be asked for your UVA computing ID. Be sure this is correct.
2. You will be asked to select an SSH key for connecting to your EC2 instance.
3. Note the outputs of your CF Stack:
   - asdf
   - asdf
   - asdf
4. asdfasdf
# AWS Deployment Design

## 1. Client (React + TS):

- Build: Use `npm run build` to build static files
- Host on **Amazon S3**
  - store the built static assets.
  - update website policy to use static websites

## 2. Server (FastAPI + Pydantic):

- Write a `Docker file` and containerize FastAPI app.
- Push this image to `ECR`
- Run it on `ECS` which is a serverless container runtime environment.

## 3. Database

- Use `Supabase` as it is or can switch to `Amazon RDS` to provide `Postgres` for chat sessions, history and user data.
- `Note: Reconfigure Login handling which currently uses Supabase to provide OAuth`
- Pinecone or other vector db. Can switch to faster pulls by using `FAISS` for in memory storage of user docs during retrieval and repeated queries, avoid querying hosted vector database

## 4. Deployment Flow

- Client: Run build -> upload `build` folder to `S3`
- Server:
  - Build `Docker` image and test.
  - push docker file to `ECS` and compose up
  - Github auto deploy actions can be added to integrate for `CI/CD`

## Additional

- Logging: Use internal setup `logger` with `DEBUG=true` to flag error details.

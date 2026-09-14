# 🚀 Deploy InsightGraph to Render (Free)

## Prerequisites

1. **GitHub Account** - Your code is already on GitHub
2. **Render Account** - Sign up at https://render.com (free)

---

## Step 1: Create Render Account

1. Go to https://render.com
2. Click **Get Started for Free**
3. Sign up with your **GitHub account**
4. Authorize Render to access your repositories

---

## Step 2: Create Backend Service

1. In Render Dashboard, click **New +** → **Web Service**
2. Connect your GitHub repository: `venya2206-tech/insightgraph`
3. Configure:
   - **Name:** `insightgraph-backend`
   - **Runtime:** `Docker`
   - **DockerfilePath:** `./backend/Dockerfile`
   - **Docker Context:** `./backend`
4. Click **Advanced** → Add Environment Variables:
   ```
   APP_ENV=production
   APP_DEBUG=false
   GROQ_API_KEY=your-groq-api-key
   ```
5. Click **Create Web Service**

---

## Step 3: Create Frontend Service

1. Click **New +** → **Web Service**
2. Connect the same repository
3. Configure:
   - **Name:** `insightgraph-frontend`
   - **Runtime:** `Docker`
   - **DockerfilePath:** `./frontend/Dockerfile`
   - **Docker Context:** `./frontend`
4. Click **Advanced** → Add Environment Variables:
   ```
   NEXT_PUBLIC_API_URL=https://insightgraph-backend.onrender.com
   ```
5. Click **Create Web Service**

---

## Step 4: Set Up Databases

### PostgreSQL (Free)
1. Click **New +** → **PostgreSQL**
2. Name: `insightgraph-db`
3. Database: `insightgraph`
4. User: `insightgraph`
5. Note the **Internal Database URL**

### Neo4j (Free)
1. Sign up at https://neo4j.com/cloud/aura-free/
2. Create a free instance
3. Note the **Bolt URL**, **Username**, and **Password**

### Redis (Free)
1. Sign up at https://redis.com/try-free/
2. Create a free database
3. Note the **Connection URL**

---

## Step 5: Update Backend Environment Variables

Go to your backend service in Render → **Environment** tab, add:

```
DATABASE_URL=<your-postgres-internal-url>
NEO4J_URI=bolt://<your-neo4j-url>
NEO4J_USER=<your-neo4j-username>
NEO4J_PASSWORD=<your-neo4j-password>
REDIS_URL=<your-redis-url>
GROQ_API_KEY=<your-groq-api-key>
```

**Get your Groq API key from:** https://console.groq.com

---

## Step 6: Deploy!

1. Render will automatically deploy when you push to GitHub
2. Wait 5-10 minutes for first deployment
3. Your URLs will be:
   - **Backend:** `https://insightgraph-backend.onrender.com`
   - **Frontend:** `https://insightgraph-frontend.onrender.com`

---

## Step 7: Test

1. Open `https://insightgraph-frontend.onrender.com`
2. Create a research project
3. Add a source
4. Generate an AI report

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | Check environment variables are correct |
| Frontend can't connect | Verify NEXT_PUBLIC_API_URL points to backend |
| Database errors | Ensure DATABASE_URL is the Internal URL, not External |

---

## Free Tier Limits

| Service | Free Limit |
|---------|------------|
| Render Web Services | 750 hours/month |
| PostgreSQL | 90 days, then pay |
| Neo4j Aura | 50K nodes |
| Redis | 30MB storage |

---

## Cost

**Total: $0/month** (within free tier limits)

---

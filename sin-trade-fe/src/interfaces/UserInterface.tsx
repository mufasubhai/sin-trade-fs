export interface User {
  accessToken: string;
  refreshToken: string;
  activeAssets: Map<string, Asset>;
  avatarUrl: string | null;
  createdAt: Date;
  email: string;
  emailConfirmedAt: Date | null;
  firstName: string | null;
  lastName: string | null;
  updatedAt: string;
  userId: string;
  username: string | null;
  website: string | null;

  // aud: authenticationStatus;
}

export interface Asset {
  asset_id: number;
  created_at: Date;
  id: number;
  ticker_name: string;
  user_id: number;
}

export function convertDataToUserObject(data: Map<string, unknown>): User {
  let isValidUser = false;

  if (
  
   
    data.has("access_token") && typeof data.get("access_token") === "string" &&
    data.has("refresh_token") && typeof data.get("refresh_token") === "string" &&
    data.has("user_id") && typeof data.get("user_id") === "string" &&
    data.has("email") && typeof data.get("email") === "string" &&

    // data.has("first_name") && typeof data.get("first_name") === "string" &&
    // data.has("last_name") && typeof data.get("last_name") === "string" &&
    // data.has("avatar_url") && typeof data.get("avatar_url") === "string" &&
    data.has("created_at") && typeof data.get("created_at") === "string" &&
    data.has("updated_at") && typeof data.get("updated_at") === "string"
  ) {
    isValidUser = true;
  }

  if (!isValidUser) {
    throw new Error("Invalid user data");
  }

  return {
    accessToken: data.get("access_token") as string,
    refreshToken: data.get("refresh_token") as string,
    activeAssets: data.get("active_assets") as Map<string, Asset>,
    avatarUrl: data.get("avatar_url") as string | null,
    createdAt: data.get("created_at") as Date,
    email: data.get("email") as string,
    emailConfirmedAt: data.get("email_confirmed_at") as Date | null,
    firstName: data.get("first_name") as string | null,
    lastName: data.get("last_name") as string | null,
    updatedAt: data.get("updated_at") as string,
    userId: data.get("user_id") as string,
    username: data.get("username") as string | null,
    website: data.get("website") as string | null,
  } as User;
} 
// enum authenticationStatus {
//   authenticated,
//   unauthenticated,
//   // we may not need these statuses
//   loading,
//   error,
// }

// {
//   "access_token": "eyJhbGciOiJIUzI1NiIsImtpZCI6Ijl5bXA2RE9GSEFBTGYwazgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3ZxYWRrY2pmcHVjcGd1Y3hlc3ZwLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJjMTdlMzk0Yy1iODhhLTRlZDctOGQzNC0wZDA0NWFmYjM3YzAiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzQwOTcxMTA0LCJpYXQiOjE3NDA5Njc1MDQsImVtYWlsIjoiYWFwb2RhY2ErMjI1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiYXZhdGFyX3VybCI6Imh0dHBzOi8vbWVkaWEubGljZG4uY29tL2Rtcy9pbWFnZS92Mi9ENTYwM0FRRWRXT3FiUmtZTlpRL3Byb2ZpbGUtZGlzcGxheXBob3RvLXNocmlua184MDBfODAwL3Byb2ZpbGUtZGlzcGxheXBob3RvLXNocmlua184MDBfODAwLzAvMTcwNjEyMTA5MzE2ND9lPTE3NDAwMDk2MDBcdTAwMjZ2PWJldGFcdTAwMjZ0PWdaU2NLdURFbmNXOGtXektLbU5uNjZ2bzdkV0xkNXpJYnY5UVVrcXJrS1EiLCJlbWFpbCI6ImFhcG9kYWNhKzIyNUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyc3RfbmFtZSI6IkFkcmlhbiIsImxhc3RfbmFtZSI6IkFwb2RhY2EiLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInN1YiI6ImMxN2UzOTRjLWI4OGEtNGVkNy04ZDM0LTBkMDQ1YWZiMzdjMCIsInVzZXJuYW1lIjoibXVmYXN1MTIyMjUiLCJ3ZWJzaXRlIjoiYWRyaWFuYXBvZGFjYS5jb20ifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTc0MDk2NzUwNH1dLCJzZXNzaW9uX2lkIjoiNDIwMTc5NTQtZjEyMi00MWNkLTkyMTMtMjRjYjM4MTU3MmFiIiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.tQ5R_wT_Ni9erfrWsbbWEn22Juwt7aCK-y1hjdDKnwo",
//   "active_assets": {
//       "BTC": {
//           "asset_id": 1,
//           "created_at": "2025-03-02T22:31:19.828433+00:00",
//           "id": 4,
//           "ticker_name": "BTC",
//           "user_id": 33
//       },
//       "ETH": {
//           "asset_id": 2,
//           "created_at": "2025-03-02T22:31:31.373852+00:00",
//           "id": 5,
//           "ticker_name": "ETH",
//           "user_id": 33
//       },
//       "SOL": {
//           "asset_id": 3,
//           "created_at": "2025-03-02T22:31:45.149832+00:00",
//           "id": 6,
//           "ticker_name": "SOL",
//           "user_id": 33
//       }
//   },
//   "avatar_url": "https://media.licdn.com/dms/image/v2/D5603AQEdWOqbRkYNZQ/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1706121093164?e=1740009600&v=beta&t=gZScKuDEncW8kWzKKmNn66vo7dWLd5zIbv9QUkqrkKQ",
//   "created_at": "2025-03-02T20:10:13.759945+00:00",
//   "email": "aapodaca+225@gmail.com",
//   "email_confirmed_at": null,
//   "first_name": "Adrian",
//   "last_name": "Apodaca",
//   "refresh_token": "sWi_3s0opBUDzIauN1c2zw",
//   "updated_at": "2025-03-03T02:05:04.594894+00:00",
//   "user_id": 33,
//   "username": "mufasu12225",
//   "website": "adrianapodaca.com"
// }

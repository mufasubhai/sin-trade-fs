export interface UserResponse {
  access_token: string; 
  aud: authentication_status;
  refresh_token: string;
  user: User;
}

export interface User {
  avatar_url: string | null;
  created_at: string;
  updated_at: string;
  username: string | null;
  website: string | null;
  email: string;
  email_verified: boolean;
  first_name: string | null;
  id: string;
  last_name: string | null;
  phone_verified: boolean;
}

enum authentication_status {
  authenticated,
  unauthenticated,
  // we may not need these statuses
  loading,
  error,
}


// {
//   "access_token": "eyJhbGciOiJIUzI1NiIsImtpZCI6Ijl5bXA2RE9GSEFBTGYwazgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3ZxYWRrY2pmcHVjcGd1Y3hlc3ZwLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJmM2U0ODRjYy0xNjU4LTQ1N2ItYmE2NS04MjRjZThjYTI4NWIiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzM1MTAyNDIwLCJpYXQiOjE3MzUwOTg4MjAsImVtYWlsIjoiYWFwb2RhY2FAZ21haWwuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6ImFhcG9kYWNhQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJzdWIiOiJmM2U0ODRjYy0xNjU4LTQ1N2ItYmE2NS04MjRjZThjYTI4NWIifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTczNTA5ODgyMH1dLCJzZXNzaW9uX2lkIjoiNzJmOTgxMmMtZmQ3NS00OTEzLTlkOGMtOTJhNDJjOTMxMDgyIiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.y-8DUCVqbFjcNjOKDgTa6A-E-U3OCrDNJ2t34r6OTJk",
//   "aud": "authenticated",
//   "refresh_token": "rGtmtmxk_K4DkhUFyYpwcA",
//   "user": {
//       "avatar_url": null,
//       "created_at": "Sun, 10 Nov 2024 23:23:45 GMT",
//       "email": "aapodaca@gmail.com",
//       "email_verified": false,
//       "first_name": null,
//       "id": "f3e484cc-1658-457b-ba65-824ce8ca285b",
//       "last_name": null,
//       "phone_verified": false,
//       "updated_at": "Wed, 25 Dec 2024 03:53:40 GMT",
//       "username": null,
//       "website": null
//   }
// }
CREATE TABLE IF NOT EXISTS giveAway (
  ServerID Integer PRIMARY KEY,
  ChannelID Integer
);

CREATE TABLE IF NOT EXISTS openAI (
  ServerID Integer PRIMARY KEY,
  APIKey text
);

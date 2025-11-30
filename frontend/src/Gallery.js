import React, { useEffect, useState } from "react";

const API_URL = "http://localhost:8000";

function Gallery({ user }) {
  const [photos, setPhotos] = useState([]);
  const [wallet, setWallet] = useState(0);
  const [selectedPhoto, setSelectedPhoto] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const userId = user.id;

  const fetchPhotos = async () => {
    const res = await fetch(`${API_URL}/photos?user_id=${userId}`);
    const data = await res.json();
    setPhotos(data);
  };

  const fetchWallet = async () => {
    const res = await fetch(`${API_URL}/wallet?user_id=${userId}`);
    const data = await res.json();
    setWallet(data);
  };

  const fetchPhotoDetail = async (photoId) => {
    const res = await fetch(`${API_URL}/photos/${photoId}?user_id=${userId}`);
    const data = await res.json();
    setSelectedPhoto(data);
  };

  const unlockPhoto = async (photoId) => {
    try {
      setLoading(true);
      setMessage("");
      const res = await fetch(`${API_URL}/unlock?user_id=${userId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ photo_id: photoId }),
      });
      const data = await res.json();
      if (!res.ok) {
        setMessage(data.detail || "Error unlocking");
      } else {
        setMessage("Unlocked!");
        setWallet(data.token_balance);
        await fetchPhotos();
        await fetchPhotoDetail(photoId);
      }
    } catch (err) {
      console.error(err);
      setMessage("Network error");
    } finally {
      setLoading(false);
    }
  };

  const addTokens = async () => {
    try {
      setLoading(true);
      setMessage("");
      const res = await fetch(`${API_URL}/wallet/add?user_id=${userId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ amount: 50 }),
      });
      const data = await res.json();
      if (!res.ok) {
        setMessage(data.detail || "Error adding tokens");
      } else {
        setWallet(data.token_balance);
        setMessage("Added 50 tokens (demo).");
      }
    } catch (err) {
      console.error(err);
      setMessage("Network error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPhotos();
    fetchWallet();
  }, []);

  return (
    <div style={{ display: "flex", gap: "2rem", padding: "1rem" }}>
      <div style={{ flex: 1 }}>
        <h2>
          Wallet: {wallet} tokens{" "}
          <button onClick={addTokens} disabled={loading}>
            Add 50 tokens (demo)
          </button>
        </h2>
        {message && <p>{message}</p>}

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(150px, 1fr))",
            gap: "1rem",
          }}
        >
          {photos.map((photo) => (
            <div
              key={photo.id}
              style={{
                border: "1px solid #ccc",
                padding: "0.5rem",
                cursor: "pointer",
              }}
              onClick={() => fetchPhotoDetail(photo.id)}
            >
              <div style={{ width: "100%", overflow: "hidden" }}>
                <img
                  src={photo.preview_url}
                  alt={photo.title}
                  style={{
                    width: "100%",
                    filter: photo.unlocked ? "none" : "blur(10px)",
                  }}
                />
              </div>
              <h4>{photo.title}</h4>
              <p style={{ fontSize: "0.9rem" }}>
                {photo.price_tokens} tokens to unlock
              </p>
              {photo.unlocked && (
                <span style={{ fontSize: "0.8rem" }}>✅ Unlocked</span>
              )}
            </div>
          ))}
        </div>
      </div>

      <div style={{ flexBasis: "320px" }}>
        <h3>Selected item</h3>
        {selectedPhoto ? (
          <div>
            <h4>{selectedPhoto.title}</h4>
            <p>{selectedPhoto.description}</p>
            <div style={{ marginBottom: "1rem" }}>
              <img
                src={
                  selectedPhoto.unlocked
                    ? selectedPhoto.original_url
                    : selectedPhoto.preview_url
                }
                alt={selectedPhoto.title}
                style={{
                  width: "100%",
                  maxWidth: "300px",
                  filter: selectedPhoto.unlocked ? "none" : "blur(10px)",
                }}
              />
            </div>
            {!selectedPhoto.unlocked && (
              <button
                onClick={() => unlockPhoto(selectedPhoto.id)}
                disabled={loading}
              >
                {loading
                  ? "Unlocking..."
                  : `Unlock for ${selectedPhoto.price_tokens} tokens`}
              </button>
            )}
            {selectedPhoto.unlocked && <p>You own this item.</p>}
          </div>
        ) : (
          <p>Select an item from the gallery.</p>
        )}
      </div>
    </div>
  );
}

export default Gallery;

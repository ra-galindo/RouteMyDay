const { createApp } = Vue;

createApp({
  data() {
    return {
      fixedStart: false,
      fixedEnd: false,
      loading: false,
      errorMsg: "",
      result: null,
      submittedPlaces: [],
      dragIndex: null,
      places: [
        { name: "Prague Castle" },
        { name: "Charles Bridge" },
      ]
    };
  },

  computed: {
    validPlaceCount() {
      return this.places.filter(p => p.name.trim()).length;
    },

    orderedPlaces() {
      if (!this.result) return [];
      return this.result.order.map(i => this.submittedPlaces[i] ?? `Stop ${i + 1}`);
    },

    estimatedTime() {
      if (!this.result) return "";
      const minutes = Math.round(this.result.total_duration_min);
      if (minutes < 60) return `${minutes} min`;
      const h = Math.floor(minutes / 60);
      const m = minutes % 60;
      return m > 0 ? `${h}h ${m}m` : `${h}h`;
    }
  },

  methods: {
    dragStart(i) {
      this.dragIndex = i;
    },

    dragOver(i) {
      if (this.dragIndex === null || this.dragIndex === i) return;
      const moved = this.places.splice(this.dragIndex, 1)[0];
      this.places.splice(i, 0, moved);
      this.dragIndex = i;
      this.result = null;
    },

    dragEnd() {
      this.dragIndex = null;
    },

    add() {
      if (this.places.length < 15) {
        this.places.push({ name: "" });
      }
    },

    remove(i) {
      if (this.places.length > 2) {
        this.places.splice(i, 1);
        this.result = null;
      }
    },

    async optimize() {
      const valid = this.places.map(p => p.name.trim()).filter(Boolean);
      if (valid.length < 2) return;

      this.loading = true;
      this.errorMsg = "";
      this.result = null;
      this.submittedPlaces = [...valid];

      try {
        const isLocal = location.hostname === "localhost" || location.hostname === "127.0.0.1" || location.protocol === "file:";
        const baseUrl = isLocal ? "http://localhost:8000" : "https://routemyday.onrender.com";
        const res = await fetch(`${baseUrl}/optimize`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            places: valid,
            fixed_start: this.fixedStart,
            fixed_end: this.fixedEnd
          })
        });

        if (!res.ok) {
          const err = await res.json().catch(() => ({}));
          throw new Error(err.detail || `Server error ${res.status}`);
        }

        this.result = await res.json();
      } catch (e) {
        console.error(e);
        this.errorMsg = e.message || "Could not reach the API. Check the backend URL in Advanced settings.";
      } finally {
        this.loading = false;
      }
    }
  }
}).mount("#app");
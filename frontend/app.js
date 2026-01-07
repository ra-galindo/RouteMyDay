const { createApp } = Vue;

createApp({
  data() {
    return {
      api: "",
      fixedEnd: false,
      status: "",
      result: null,
      places: [
        { name: "Prague Castle", lat: 50.0909, lng: 14.4006 },
        { name: "Charles Bridge", lat: 50.0865, lng: 14.4114 },
      ]
    };
  },

  methods: {
    add() {
      this.places.push({ name: "", lat: 0, lng: 0 });
    },

    remove(i) {
      this.places.splice(i, 1);
    },

    async optimize() {
      this.status = "Calculating…";
      this.result = null;

      try {
        const res = await fetch(`${this.api}/optimize`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            places: this.places,
            fixed_end: this.fixedEnd
          })
        });

        const data = await res.json();
        this.result = data;
        this.status = "Done 🎉";
      } catch (e) {
        console.error(e);
        this.status = "Error contacting API";
      }
    }
  }
}).mount("#app");

const csrftoken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute('content');

let timer;

document.querySelector(".from_value").addEventListener("input", () => {
    clearTimeout(timer);

    timer = setTimeout(async () => {
        const from_value = document.querySelector(".from_value").value;
        const from_country = document.querySelector("#from").value;
        const to_country = document.querySelector("#to").value;

        const numericValue = Number(from_value);
        if (!Number.isFinite(numericValue)) return;

        const response = await fetch("/convert_API/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                from_value: numericValue,
                from: from_country,
                to: to_country,
            }),
        });

        if (!response.ok) return;

        const data = await response.json();
        document.querySelector(".to_value").value = data.result;
    }, 400);
});

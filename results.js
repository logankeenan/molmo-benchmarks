const fs = require('fs');

// Path to the JSON file
const filePath = './4090.json';

// Read the JSON file
fs.readFile(filePath, 'utf8', (err, data) => {
  if (err) {
    console.error(`Error reading file: ${err}`);
    return;
  }

  try {
    // Parse the JSON data
    const results = JSON.parse(data);

    // Filter results for 'test-image_50.png'
        const filteredResults = results.filter((entry) =>
      entry.image_name === 'test-image_50.png' &&
      entry.model_used === 'allenai/Molmo-7B-O-0924' &&
      entry.enable_bits_and_bytes === false
    );

    // Display the filtered results
    console.log(`Filtered results for 'test-image_50.png':\n`, filteredResults);
  } catch (parseError) {
    console.error(`Error parsing JSON: ${parseError}`);
  }
});

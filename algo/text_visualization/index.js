// Replace these variables with your actual URLs
const cirrus_url = "your_cirrus_url";
const response_url = "your_response_url";
const summary_url = "your_summary_url";
const CorpusCollocates_url = "your_corpus_collocates_url";

// Set the iframe sources dynamically
document.getElementById('cirrusFrame').src = cirrus_url;
document.getElementById('trendsFrame').src = response_url + "&view=Trends";
document.getElementById('summaryFrame').src = summary_url;
document.getElementById('collocatesFrame').src = CorpusCollocates_url;
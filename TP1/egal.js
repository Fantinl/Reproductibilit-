const fs = require('fs');

let equalCount = 0;
const total = 10000;

for (let i = 0; i < total; i++) {
    const x = Math.random() * 100;
    const y = Math.random() * 100;
    const z = Math.random() * 100;

    if ((x + y) + z === x + (y + z)) {
        equalCount++;
    }
}

const percentage = (equalCount / total) * 100;

const result = `Nombre de triplets : ${total}
Nombre d'égalités : ${equalCount}
Pourcentage d'égalité : ${percentage.toFixed(2)} %
`;

fs.writeFileSync('answer_associativity_llm.txt', result);

console.log(result);
// this example uses the en_US hunspell files from SCOWL:
//   http://wordlist.sourceforge.net/
var SpellCheck = require('spellcheck'),
    base = __dirname + (process.platform === 'win32' ? '\\' : '/'),
    spell = new SpellCheck(base + 'en_US.aff', base + 'en_US.dic');

spell.check('saint', function(err, correct, suggestions) {
    if (err) throw err;
    if (correct)
      console.log('Word is spelled correctly!');
    else
      console.log('Word not recognized. Suggestions: ' + suggestions);
});

// output:
// Word not recognized. 
// Suggestions: chain,sin,saint,satin,stain,slain,swain,rain,sail,lain,said,gain,main,spin,pain
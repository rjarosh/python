/*

bassCoupler script for MainStage/Logic Pro's scripter plugin:

This script recreates the "bass coupler" piston of that of an organ. The lowest note played will sound
while notes above the held down note are discarded.


©2024 robertjarosh

*/

// array to hold notes currently held down
var notesPlaying = [];

function HandleMIDI(event) {
    if (event instanceof NoteOn) {
        // add the note to the array (int)
        Trace("note:" + event.pitch);
        notesPlaying.push(event.pitch);
        Trace("array:" + notesPlaying);

        // unpack the array and find the lowest note
        var lowestNote = Math.min(...notesPlaying);

        // check if the current note is not the lowest
        if (event.pitch !== lowestNote) {
             // exit the function and don't sound the note
            return;
        }
    } else if (event instanceof NoteOff) {
        // remove the note from the array when no longer held down
        notesPlaying = notesPlaying.filter(note => note !== event.pitch);
    }

    // send the event if not already exited from function earlier (i.e. lowest note)
    event.send();
}

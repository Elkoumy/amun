import au.qut.apromore.automaton.Automaton;
import au.qut.apromore.automaton.Transition;
import au.qut.apromore.importer.ImportEventLog;
import org.deckfour.xes.model.XLog;

import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.Map;

public class test {
    /**
     * To remove the signature from the jar
     zip -d ./untitled1.jar 'META-INF/*.SF' 'META-INF/*.RSA' 'META-INF/*SF'

     */
    public static void main(String [] args) throws Exception {
        ImportEventLog importer = new ImportEventLog();
//        String path = "C:\\Gamal Elkoumy\\PhD\\OneDrive - Tartu Ülikool\\Differential Privacy\\amun\\data";
//        String fileName = "BPIC15_t.xes";
        String path=args[0];
        String fileName= args[1];

//        System.out.print(path);
//        System.out.print("*************");
        XLog log = importer.importEventLog(path + "\\" + fileName);
        Automaton automaton = importer.createDAFSAfromLog(log);
        String transitions = "";
        for (Map.Entry<Integer, Transition> entry : automaton.transitions().entrySet()) {
            transitions = transitions + entry.getValue().source().id() + ";" +
                    automaton.eventLabels().get(entry.getValue().eventID()) + ";" +
                    entry.getValue().target().id() + "\n";
        }

        try (PrintStream out = new PrintStream(new FileOutputStream(path + "\\" + fileName + ".txt"))) {
            out.print(transitions);
        }
        System.out.print("Done");
    }
}

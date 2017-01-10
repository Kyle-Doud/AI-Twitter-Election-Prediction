
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.parser.nndep.DependencyParser;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import edu.stanford.nlp.trees.GrammaticalStructure;
import edu.stanford.nlp.util.logging.Redwood;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.PrintWriter;
import java.io.StringReader;
import java.util.List;
import java.util.Locale;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Demonstrates how to first use the tagger, then use the NN dependency
 * parser. Note that the parser will not work on untagged text.
 *
 * @author Jon Gauthier
 * @edited 11/23/16 Kyle Doud
 * edited demo of Stanford parser from documentation
 */
public class Main  {

	/** A logger for this class */
	private static Redwood.RedwoodChannels log = Redwood.channels(Main.class);

	public static void main(String[] args) {
		String modelPath = DependencyParser.DEFAULT_MODEL;
		String taggerPath = "edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger";

		for (int argIndex = 0; argIndex < args.length; ) {
			switch (args[argIndex]) {
			case "-tagger":
				taggerPath = args[argIndex + 1];
				argIndex += 2;
				break;
			case "-model":
				modelPath = args[argIndex + 1];
				argIndex += 2;
				break;
			default:
				throw new RuntimeException("Unknown argument " + args[argIndex]);
			}
		}

		MaxentTagger tagger = new MaxentTagger(taggerPath);
		DependencyParser parser = DependencyParser.loadFromModelFile(modelPath);


		try
		{
			BufferedReader tweetReader = new BufferedReader(new FileReader(new File("newData.txt")));
			PrintWriter writer = new PrintWriter("negateWords.txt", "UTF-8");
			String line;
			int lineNum = 1;
			while ((line = tweetReader.readLine()) != null)
			{
				//System.out.println(line);
				if(line.toLowerCase().contains(" not "))
				{
					DocumentPreprocessor tokenizer = new DocumentPreprocessor(new StringReader(line));
					for (List<HasWord> sentence : tokenizer) 
					{
						List<TaggedWord> tagged = tagger.tagSentence(sentence);
						GrammaticalStructure gs = parser.predict(tagged);
						// Print typed dependencies
						String grammar = gs.toString().toLowerCase();
						Matcher m = Pattern.compile("\\((.*?)\\)").matcher(grammar);
						String inParens = "";
						while(m.find()) 
						{
							if(m.group(1).contains("not"))
							{
								inParens = m.group(1);
							}
						}
						try{
						String[] parts = inParens.split(", ");
						String wordWeWant = parts[0].contains("not") ? parts[1] : parts[0];
						wordWeWant = wordWeWant.substring(0, wordWeWant.indexOf("-"));
			
						writer.println(lineNum + " " + wordWeWant);}
						catch(Exception a)
						{
							//lineNum++;
							continue;
						}
						//log.info(gs);
					}
				}
				lineNum++;
			}
			tweetReader.close();
			writer.close();
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}


	}

}
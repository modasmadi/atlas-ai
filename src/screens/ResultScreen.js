import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, Image, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS, SPACING } from '../constants/theme';
import GradientButton from '../components/GradientButton';
import { ArrowLeft, Share2, Copy } from 'lucide-react-native';

export default function ResultScreen({ route, navigation }) {
    const { type, uri, name } = route.params;
    const [loading, setLoading] = useState(true);

    // Mock AI Response
    const [response, setResponse] = useState('');

    useEffect(() => {
        // Simulate AI Processing time
        setTimeout(() => {
            setResponse(
                type === 'image'
                    ? "Based on the image provided, this appears to be a calculus problem involving derivatives. \n\n**Solution:**\nTo solve d/dx(x^2 + 3x), we apply the power rule:\n1. The derivative of x^2 is 2x.\n2. The derivative of 3x is 3.\n\n**Final Answer:**\n2x + 3\n\n**Explanation:**\nThe power rule states that d/dx(x^n) = nx^(n-1). Applying this to each term gives us the linear function representing the slope."
                    : `I have analyzed the file "${name}". \n\n**Summary:**\nThis document covers the fundamentals of Quantum Mechanics. Key points include:\n- Wave-particle duality\n- Schrödinger equation\n- Heisenberg uncertainty principle.\n\n**Key Questions extracted:**\n1. What is a wave function?\n2. Define quantum superposition.`
            );
            setLoading(false);
        }, 3000);
    }, []);

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.header}>
                <ArrowLeft color={COLORS.text} size={24} onPress={() => navigation.goBack()} />
                <Text style={styles.headerTitle}>Analysis Result</Text>
                <Share2 color={COLORS.text} size={24} />
            </View>

            <ScrollView contentContainerStyle={styles.content}>
                {type === 'image' && (
                    <Image source={{ uri }} style={styles.previewImage} resizeMode="contain" />
                )}

                {type === 'document' && (
                    <View style={styles.filePreview}>
                        <Text style={styles.fileName}>{name}</Text>
                        <Text style={styles.fileType}>PDF Document</Text>
                    </View>
                )}

                <View style={styles.resultCard}>
                    {loading ? (
                        <View style={styles.loadingContainer}>
                            <ActivityIndicator size="large" color={COLORS.primary} />
                            <Text style={styles.loadingText}>Analyzing your {type}...</Text>
                            <Text style={styles.loadingSubtext}>Our AI is working its magic</Text>
                        </View>
                    ) : (
                        <>
                            <View style={styles.resultHeader}>
                                <Text style={styles.resultTitle}>AI Answer</Text>
                                <Copy color={COLORS.textSecondary} size={20} />
                            </View>
                            <Text style={styles.resultText}>{response}</Text>

                            <View style={styles.actions}>
                                <GradientButton title="Ask Follow-up" onPress={() => { }} style={{ marginTop: SPACING.l }} />
                            </View>
                        </>
                    )}
                </View>
            </ScrollView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: COLORS.background,
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: SPACING.l,
        borderBottomWidth: 1,
        borderBottomColor: COLORS.surfaceLight,
    },
    headerTitle: {
        color: COLORS.text,
        fontSize: 18,
        fontWeight: 'bold',
    },
    content: {
        padding: SPACING.l,
    },
    previewImage: {
        width: '100%',
        height: 200,
        borderRadius: 16,
        marginBottom: SPACING.l,
        backgroundColor: COLORS.surface,
    },
    filePreview: {
        backgroundColor: COLORS.surface,
        padding: SPACING.l,
        borderRadius: 16,
        marginBottom: SPACING.l,
        borderLeftWidth: 4,
        borderLeftColor: COLORS.secondary,
    },
    fileName: {
        color: COLORS.text,
        fontSize: 16,
        fontWeight: 'bold',
    },
    fileType: {
        color: COLORS.textSecondary,
        fontSize: 14,
        marginTop: 4,
    },
    resultCard: {
        backgroundColor: COLORS.surface,
        borderRadius: 20,
        padding: SPACING.l,
        minHeight: 300,
    },
    loadingContainer: {
        alignItems: 'center',
        justifyContent: 'center',
        height: 200,
    },
    loadingText: {
        color: COLORS.text,
        fontSize: 18,
        fontWeight: 'bold',
        marginTop: SPACING.m,
    },
    loadingSubtext: {
        color: COLORS.textSecondary,
        marginTop: SPACING.xs,
    },
    resultHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: SPACING.m,
    },
    resultTitle: {
        color: COLORS.success, // Green for "Solved"
        fontSize: 20,
        fontWeight: 'bold',
    },
    resultText: {
        color: COLORS.text,
        fontSize: 16,
        lineHeight: 24,
    },
});
